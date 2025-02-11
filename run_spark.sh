#!/bin/bash

# local run
#export SPARK_HOME=/opt/spark
#export PATH=$SPARK_HOME/bin:$PATH

#spark-submit --master local[*] --packages org.postgresql:postgresql:42.6.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 src/main/read_stream_to_db.py

docker exec -it python-app spark-submit \
 --master spark://spark-master:7077 \
 --packages org.postgresql:postgresql:42.6.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
 --total-executor-cores 2 \
 main/read_stream_to_db.py