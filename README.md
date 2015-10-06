# EasyRide
## Introduction

[EasyRide] (http://easyride.us) is a real-time data platform to connect people for easy ridesharing. It shows the locations of available drivers and riders on a map and users can search for nearby drivers/riders. It also simulates the real-time driver/rider matching in the back end.
![Project Overview] (flask/app/static/images/overview.png)

## Data

The rideshare requests are engineered with the schema shown below. The drivers and riders are being matched based on their starting locations and destinations.
![Sample Data] (flask/app/static/images/sampledata.png)

## Data Pipeline

![Data Pipeline] (flask/app/static/images/pipeline.png)

## Distributed AWS Clusters
The following cluster configuration is used in this project:
* 4 m4.large for data ingestion using [Kafka] (http://kafka.apache.org/) and [Spark Streaming] (http://spark.apache.org/streaming/) for real-time processing.
* 4 m4.large for [Elasticsearch] (https://www.elastic.co/products/elasticsearch) 
* 1 t2.micro for the font end using [flask] (http://flask.pocoo.org/)

## Live Demo
A live demo of the project and the presentation slides can be found at [easyride.us] (http://easyride.us)

## Usage
1. Start Spark on the Spark Cluster: $SPARK_HOME/sbin/start-all.sh
2. Then start Spark Streaming job: "spark-submit --class StreamProject --master spark://ip-172-31-2-139:7077 --jars target/scala-2.10/ride_messages-assembly-1.0.jar target/scala-2.10/ride_messages_2.10-1.0.jar"
3. Start Elasticsearch on the database cluster: sudo $ELASTICSEARCH_HOME/bin/elasticsearch &
4. Create Elasticsearch database with specified index and type
5. Start kafka producer and simulation: ./simulation.sh
6. Stop kafka producer and simulation: ./stop.sh
