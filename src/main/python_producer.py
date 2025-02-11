import json
import time
import urllib.request
from utils import load_config as lc
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import os


class KafkaProducerWrapper:
    """
    A wrapper class for Kafka producer functionality.
    """

    def __init__(self, broker: str, topic: str):
        """
        Initialize the Kafka producer.

        :param broker: Kafka broker address (e.g., "broker:9092").
        :param topic: Kafka topic to produce messages to.
        """
        self.broker = broker
        self.topic = topic
        self.producer = None

    def check_kafka_connection(self) -> bool:
        """
        Check if the Kafka broker is available.

        :return: True if the broker is available, False otherwise.
        """
        try:
            # Attempt to create a Kafka producer
            producer = KafkaProducer(bootstrap_servers=self.broker)
            producer.close()
            return True
        except NoBrokersAvailable:
            return False

    def create_producer(self):
        """
        Create a Kafka producer.
        """
        self.producer = KafkaProducer(bootstrap_servers=self.broker)

    def send_message(self, message: str):
        """
        Send a message to the Kafka topic.

        :param message: The message to send.
        """
        if self.producer:
            self.producer.send(self.topic, message.encode())
        else:
            raise RuntimeError("Kafka producer is not initialized.")

    def close(self):
        """
        Close the Kafka producer.
        """
        if self.producer:
            self.producer.close()


class VelibStationsProducer:
    """
    A class to fetch Velib station data from an API and send it to Kafka.
    """

    def __init__(self, api_url: str, kafka_producer: KafkaProducerWrapper):
        """
        Initialize the Velib stations producer.

        :param api_url: The URL to fetch Velib station data from.
        :param kafka_producer: An instance of KafkaProducerWrapper.
        """
        self.api_url = api_url
        self.kafka_producer = kafka_producer

    def fetch_stations_data(self):
        """
        Fetch Velib station data from the API.

        :return: A list of station data.
        """
        response = urllib.request.urlopen(self.api_url)
        return json.loads(response.read().decode())

    def produce_stations_data(self):
        """
        Fetch data from the API and send it to Kafka.
        """
        while True:
            try:
                # Fetch data from the API
                stations = self.fetch_stations_data()

                # Send data to Kafka topic
                for station in stations:
                    self.kafka_producer.send_message(json.dumps(station))

                print("Json data : \n", json.dumps(station, indent=4))
                # print("{} Produced {} station records".format(time.time(), len(stations)))

                # Wait before fetching data again
                time.sleep(2)

            except Exception as e:
                print(f"Error occurred: {e}. Retrying in 5 seconds...")
                time.sleep(5)


if __name__ == "__main__":
    # Load configuration
    app_config = lc.read_config_params(config_file_path='./main/app_conf.ini')
    API_KEY = app_config['JC_DECAUX_API']['key']
    URL = app_config['JC_DECAUX_API']['url'] + API_KEY
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "broker:9092")
    KAFKA_TOPIC = app_config['kafka_broker']['topic']

    # Initialize Kafka producer wrapper
    kafka_producer = KafkaProducerWrapper(broker=KAFKA_BROKER, topic=KAFKA_TOPIC)

    # Wait for Kafka broker to become available
    while not kafka_producer.check_kafka_connection():
        print("Kafka broker not available. Retrying in 5 seconds...")
        time.sleep(5)

    print("Kafka broker is available. Starting producer...")
    kafka_producer.create_producer()

    # Initialize Velib stations producer
    velib_producer = VelibStationsProducer(api_url=URL, kafka_producer=kafka_producer)

    # Start producing data
    velib_producer.produce_stations_data()