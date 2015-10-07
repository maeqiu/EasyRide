#!/usr/bin/python
'''
Created on Oct 1, 2015

@author: maeq
'''
import random
import time
from SimulateUtilities import simulateUser
from pyelasticsearch import ElasticSearch

NUM_MESSAGES = 1000000
es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")#messageid=1
    
while True:
    messageid=random.choice(range(NUM_MESSAGES))
    drflag=random.choice([0, 1])
    print "New user comes in, messageid = %d, drflag = %d" % (messageid, drflag)
    
    query = { 
            "query": {
               "bool" : {
                 "must" : [
                    { "match": { "drflag": drflag } }, 
                    { "match": { "messageid": messageid } }
                  ]
                }
             }
            }
        
    print "-----------randomly pick a messageid from the database-----------"
    res = es_client.search(query, index='messages', doc_type='myMessages')    
    hits = res['hits']['hits']
                            
    deplat=[]
    deplon=[]
    arrlat=[]
    arrlon=[]
     
    if len(hits) != 0:            # with drivers/riders in the database      
        for re in hits:
            phone = re['_source']['phone']
            deplat.append(re['_source']['deplocation']['lat'])
            deplon.append(re['_source']['deplocation']['lon'])
            arrlat.append(re['_source']['arrlocation']['lat'])
            arrlon.append(re['_source']['arrlocation']['lon'])
        drflag = 1-drflag    #convert from driver->rider or rider->driver
        producer = simulateUser(es_client, 'messages', 'myMessages', (deplat[0],deplon[0]), (arrlat[0],arrlon[0]), drflag)
        producer.simulating()
    else:
        print "no record found, retrying!"
    
    time.sleep(1)


