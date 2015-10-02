import json
import random
import sys
import time

from pyelasticsearch import ElasticSearch

class retrieveLocations(object):
    def __init__(self, esindex, drflag):
        self.esindex = esindex
        self.drflag = drflag
            
    def retrieving(self):
        es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
        # construct query to list all drivers/riders
        querySize = 15
        query = { 
                "size": querySize,
                "query": { "match": { "drflag": self.drflag } }
                }
    
        print "-----------executing search query-----------"
        res = es_client.search(query, index=self.esindex)    
        hits = res['hits']['hits']
                        
        deplat=[]
        deplon=[]
        arrlat=[]
        arrlon=[]
                
        if len(hits) != 0:            # with drivers/riders in the database      
            for re in hits:
                name = re['_source']['name']
                deplat.append(re['_source']['deplocation']['lat'])
                deplon.append(re['_source']['deplocation']['lon'])
                arrlat.append(re['_source']['arrlocation']['lat'])
                arrlon.append(re['_source']['arrlocation']['lon'])
        return (deplat, deplon, arrlat, arrlon)
        
