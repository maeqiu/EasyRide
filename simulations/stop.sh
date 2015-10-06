#!/usr/bin/env bash

screen -ls | grep kafkaProducer | cut -d. -f1 | awk '{print $1}' | xargs kill -9
screen -ls | grep simulateUser | cut -d. -f1 | awk '{print $1}' | xargs kill -9
screen -wipe

