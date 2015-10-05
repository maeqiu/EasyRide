# EasyRide
## Introduction

EasyRide is a real-time data platform to connect people for easy ridesharing. It shows the locations of available drivers and riders on a map and users can search for nearby drivers/riders. It also simulates the real-time driver/rider matching in the back end.
![Project Overview] (flask/static/images/overview.png)

## Data

The rideshare requests are engineered with the schema shown below. The drivers and riders are being matched based on their starting locations and destinations.
![Sample Data] (flask/static/images/sampledata.png)

## Data Pipeline

![Data Pipeline] (flask/static/images/pipeline.png)

## Distributed AWS Clusters
The following cluster configuration is used in this project:
* 4 m4.large for data ingestion using [Kafka] (http://kafka.apache.org/) and [Spark Streaming] (http://spark.apache.org/streaming/) for real-time processing.
* 4 m4.large for [Elasticsearch] (https://www.elastic.co/products/elasticsearch) 
* 1 t2.micro for the font end using [flask] (http://flask.pocoo.org/)
