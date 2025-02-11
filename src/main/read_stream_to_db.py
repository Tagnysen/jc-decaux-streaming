from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType, DoubleType, LongType
from utils import load_config as lc
import os

class ConfigLoader:
    """Class to load application configurations."""

    def __init__(self, config_path: str = './main/app_conf.ini') -> None:
        """
        Load configuration parameters from the given file path.
        
        """
        # Config path
        self.app_config = lc.read_config_params(config_file_path=config_path)
        
        # PostgreSQL Config
        self.USER: str = self.app_config['postgres']['user']
        self.PASSWORD: str = self.app_config['postgres']['password']
        self.DATABASE: str = self.app_config['postgres']['db']
        self.TABLE: str = self.app_config['postgres']['table']
        self.PORT: int = int(self.app_config['postgres']['port'])
        self.POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
        self.DB_URL: str = f"jdbc:postgresql://{self.POSTGRES_HOST}:{self.PORT}/{self.DATABASE}"

        # Kafka Config
        self.KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "broker:9092")
        self.KAFKA_TOPIC: str = self.app_config['kafka_broker']['topic']

class SparkKafkaProcessor:
    """
    Handle Spark streaming from Kafka and writing to PostgreSQL.
    
    """
    
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.spark: SparkSession = self._initialize_spark_session()
        self.schema: StructType = self._define_schema()
    
    def _initialize_spark_session(self) -> SparkSession:
        """
        Initialize and return a Spark session.
        
        """

        return SparkSession.builder \
            .appName("KafkaPostgresStreaming") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.6.0") \
            .getOrCreate()

    def _define_schema(self) -> StructType:
        """
        Define and return the schema for incoming Kafka JSON messages.
        
        """

        return StructType([
            StructField("number", IntegerType(), True),
            StructField("contract_name", StringType(), True),
            StructField("name", StringType(), True),
            StructField("address", StringType(), True),
            StructField("position", StructType([
                StructField("lat", DoubleType(), True),
                StructField("lng", DoubleType(), True)
            ]), True),
            StructField("banking", BooleanType(), True),
            StructField("bonus", BooleanType(), True),
            StructField("bike_stands", IntegerType(), True),
            StructField("available_bike_stands", IntegerType(), True),
            StructField("available_bikes", IntegerType(), True),
            StructField("status", StringType(), True),
            StructField("last_update", LongType(), True)
        ])

    def read_from_kafka(self) -> DataFrame:
        """
        Read data stream from Kafka topic and return a DataFrame.
        
        """
        
        return self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.config.KAFKA_BROKER) \
            .option("subscribe", self.config.KAFKA_TOPIC) \
            .option("startingOffsets", "latest") \
            .load()

    def transform_data(self, df: DataFrame) -> DataFrame:
        """
        Parse JSON messages and extract relevant fields from the Kafka DataFrame.
        
        """

        return df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), self.schema).alias("data")) \
            .select(
                col("data.number"),
                col("data.contract_name"),
                col("data.name"),
                col("data.address"),
                col("data.position.lat").alias("lat"),  
                col("data.position.lng").alias("lng"),  
                col("data.banking"),
                col("data.bonus"),
                col("data.bike_stands"),
                col("data.available_bike_stands"),
                col("data.available_bikes"),
                col("data.status"),
                col("data.last_update")
            )

    def write_to_postgres(self, df: DataFrame, epoch_id: int) -> None:
        """
        Write transformed data to PostgreSQL.
        
        """

        df.write.format("jdbc") \
            .option("url", self.config.DB_URL) \
            .option("dbtable", self.config.TABLE) \
            .option("user", self.config.USER) \
            .option("password", self.config.PASSWORD) \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()

    def start_streaming(self) -> None:
        """
        Start Kafka stream processing and write to PostgreSQL.
        
        """

        kafka_df = self.read_from_kafka()
        transformed_df = self.transform_data(kafka_df)
        query = transformed_df.writeStream \
            .foreachBatch(self.write_to_postgres) \
            .outputMode("append") \
            .start()
        query.awaitTermination()

if __name__ == "__main__":
    config = ConfigLoader()
    processor = SparkKafkaProcessor(config)
    processor.start_streaming()
