#!/usr/bin/python
'''
Created on Sep 15, 2015

@author: maeq
'''
import random
import sys
import six
import time
import logging
import json
from faker import Factory
import RandomUtilities as rutil
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

fake = Factory.create()
NUM_USERS = 100
RADIUS = 50000
LATDEP = 37.061283
LONGDEP = -120.847512
LATARR = 37.957006
LONGARR = -121.291664

#logging.basicConfig(
#    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
#    level=logging.DEBUG
#)

class Producer(object):

    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = SimpleProducer(self.client)
        self.latlist1, self.lonlist1 = rutil.randomLatLon(LATDEP, LONGDEP, RADIUS, NUM_USERS)
        self.latlist2, self.lonlist2 = rutil.randomLatLon(LATARR, LONGARR, RADIUS, NUM_USERS)

    def produce_msgs(self):
        
        msg_cnt = 0
        while msg_cnt<NUM_USERS:
            timestamp=rutil.randomDate("2015,09,01,00,00,00", "2015,09,08,23,59,00", random.random())
            phone = fake.phone_number()

            message_info = rutil.create_json_message(phone=phone,                                            
                                           latdep=self.latlist1[msg_cnt],
                                           longdep=self.lonlist1[msg_cnt],
                                           latarr=self.latlist2[msg_cnt],
                                           longarr=self.lonlist2[msg_cnt],
                                           timestamp=timestamp,
                                           dr_flag=random.choice([0, 1]),
                                           user_id=random.choice(range(NUM_USERS)),
                                           message_id=msg_cnt)
            print message_info
            self.producer.send_messages('RideRequests',message_info)
            msg_cnt += 1

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    prod = Producer(ip_addr)
    prod.produce_msgs() 
