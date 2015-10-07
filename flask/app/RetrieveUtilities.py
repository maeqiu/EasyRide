import json
import random
import sys
import time

class retrieveLocations(object):
    def __init__(self, es_client, esindex, estype, drflag):
        self.client=es_client        
        self.index = esindex
        self.type = estype
        self.drflag = drflag
            
    def retrieving(self):
        # construct query to list all drivers/riders
        querySize = 15
        query = { 
                "size": querySize,
                "sort": [
                    { "date": { "order": "desc" }},
                    { "time": { "order": "desc" }}
                 ],
                "query": { "match": { "drflag": self.drflag } }
                }
    
        print "-----------executing search query-----------"
        res = self.client.search(query, index=self.index, doc_type=self.type)    
        hits = res['hits']['hits']
        
        deplat=[]
        deplon=[]
        arrlat=[]
        arrlon=[]
                
        if len(hits) != 0:            # with drivers/riders in the database      
            for re in hits:
                deplat.append(re['_source']['deplocation']['lat'])
                deplon.append(re['_source']['deplocation']['lon'])
                arrlat.append(re['_source']['arrlocation']['lat'])
                arrlon.append(re['_source']['arrlocation']['lon'])
        return (deplat, deplon, arrlat, arrlon)
        
