import json
import random
import sys
import time

from pyelasticsearch import ElasticSearch

class updateByMessageid(object):
    def __init__(self, esindex, estype, messageid):
        self.index = esindex
        self.type = estype
        self.messageid = messageid
            
    def updating(self):
        es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
        query = { 
                "query": { "match": { "messageid": self.messageid } }
                }
    
        print "-----------updating database by messageid-----------"
        res = es_client.search(query, index=self.index)
        hits = res['hits']['hits']
        for re in hits:
            print re['_id']
            es_client.delete(self.index, self.type, re['_id'])

class updateByLatLon(object):
    def __init__(self, esindex, estype, lat, lon):
        self.index = esindex
        self.type = estype
        self.lat = lat
        self.lon = lon
            
    def updating(self):
        es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
        query = { 
                "query": {
                "filtered" : {
                    "query" : {
                        "match_all" : {}
                    },
                      "filter" : {
                           "geo_distance" : {
                               "distance" : "0.01km",
                            "deplocation" : {
                                "lat" : self.lat, 
                                "lon" : self.lon
                            }
                           }
                      }
                    }
                  }
                }
    
        print "-----------updating database by Departing lat/lon-----------"
        res = es_client.search(query, index=self.index)
        hits = res['hits']['hits']
        for re in hits:
            print re['_id']
            es_client.delete(self.index, self.type, re['_id'])
                