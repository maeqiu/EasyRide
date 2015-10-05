#!/usr/bin/env bash

screen -d -m -S kafkaProducer ../kafka/kafka_producer.py ec2-52-8-225-175.us-west-1.compute.amazonaws.com:9092

screen -d -m -S simulateUser ../flask/app/run_simulate.py
