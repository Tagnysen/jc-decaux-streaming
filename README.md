# Kafka to PostgreSQL Streaming with PySpark

## 📌 Project Overview
This project is a real-time data pipeline that reads JSON data from an **Apache Kafka** topic, processes it using **Apache Spark Structured Streaming**, and stores the results in a **PostgreSQL** database. The data consists of bike station information, including location, availability, and status.

## 🚀 Features
- **Kafka Consumer**: Reads real-time data from Kafka topics.
- **Schema Handling**: Extracts necessary fields, including latitude (`lat`) and longitude (`lng`), while ignoring nested structures.
- **Spark Streaming**: Processes data in micro-batches.
- **PostgreSQL Storage**: Writes transformed data to a PostgreSQL table.


## ⚙️ Technologies Used
- **Apache Kafka** - Message broker for real-time data streaming.
- **Apache Spark** - Streaming framework for processing Kafka data.
- **PostgreSQL** - Relational database to store processed data.
- **Python 3.11** - Programming language.
- **Docker** - Containerized setup for services.

## ⚙️ Spark Standalone Architecture

<img src="SparkRuntime.png" alt="archi_server" style="width:700px;"/>


## 🔧 Configuration
Modify the `app_conf.ini` file with your PostgreSQL and Kafka details:
```ini
[postgres]
user = postgres
password = mypassword
db = bikedata
table = stations
port = 5432

[kafka_broker]
topic = bike_status
```

📊 Data Flow

1. Kafka receives JSON messages containing bike station information.
2. Spark reads the stream, extracts lat and lng, and transforms the data.
3. The processed data is inserted into a PostgreSQL table.
4. The system runs continuously to handle new messages.


