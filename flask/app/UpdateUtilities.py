import json
import random
import sys
import time
    
class updateByMessageid(object):
    def __init__(self, es_client, esindex, estype, messageid):
        self.client=es_client
        self.index = esindex
        self.type = estype
        self.messageid = messageid
            
    def updating(self):
        query = { 
                "query": { "match": { "messageid": self.messageid } }
                }
    
        print "-----------updating database by messageid-----------"
        res = self.client.search(query, index=self.index, doc_type=self.type)
        hits = res['hits']['hits']
        if len(hits)==0:
            return 1
        else:
            self.client.delete(self.index, self.type, hits[0]['_id'])
            return 0

class mark4deletionByLatLon(object):
    def __init__(self, es_client, esindex, estype, lat, lon):
        self.client=es_client
        self.index = esindex
        self.type = estype
        self.lat = lat
        self.lon = lon
            
    def marking(self):
        query = {
                "sort" : [
                      {
                          "_geo_distance" : {
                              "deplocation" : {
                                    "lat" : self.lat,
                                    "lon" : self.lon
                              }, 
                              "order" : "asc",
                              "unit" : "km"
                          }
                      }
                ], 
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

    
        print "-----------mark for deletion by LatLon-----------"
        res = self.client.search(query, index=self.index, doc_type=self.type)
        hits = res['hits']['hits']
        if len(hits)==0:
            return 1
        else:
            #self.client.delete(self.index, self.type, hits[0]['_id'])
            return hits[0]['_id']
        
class updateByLatLon(object):
    def __init__(self, es_client, esindex, estype, lat, lon):
        self.client=es_client
        self.index = esindex
        self.type = estype
        self.lat = lat
        self.lon = lon
            
    def updating(self):
        query = {
                "sort" : [
                      {
                          "_geo_distance" : {
                              "deplocation" : {
                                    "lat" : self.lat,
                                    "lon" : self.lon
                              }, 
                              "order" : "asc",
                              "unit" : "km"
                          }
                      }
                ], 
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
        res = self.client.search(query, index=self.index, doc_type=self.type)
        hits = res['hits']['hits']
        print json.dumps(hits)
        if len(hits) == 0:
            print "this driver has been picked up"
            return 1
        else:
            print hits[0]['_id']
            #remove the closest point based on distance
            self.client.delete(self.index, self.type, hits[0]['_id'])
            print "after es_client.delete"
            return 0
            
                