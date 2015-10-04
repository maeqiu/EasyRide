import json
import random
import sys
import time

class matchRides(object):
    def __init__(self, es_client, esindex, estype, deploc, arrloc, drflag):
        self.client=es_client
        self.index = esindex
        self.type = estype
        self.deplocation = deploc
        self.arrlocation = arrloc
        self.drflag = drflag
            
    def matching(self):
        # construct query to select closest drivers/riders
        query = {
          "sort" : [
              {
                  "_geo_distance" : {
                      "deplocation" : {
                            "lat" : self.deplocation[0],
                            "lon" : self.deplocation[1]
                      }, 
                      "order" : "asc",
                      "unit" : "km"
                  }
              },
              {
                  "_geo_distance" : {
                      "arrlocation" : {
                            "lat" : self.arrlocation[0],
                            "lon" : self.arrlocation[1]
                      }, 
                      "order" : "asc",
                      "unit" : "km"
                  }
              }
          ],
            "query": {
                "filtered" : {
                    "query" : {
                        "match": { "drflag": self.drflag }
                    },
                    "filter" : {
                        "bool" : {
                          "must" : [
                             { "geo_distance" : {
                                    "distance" : "20mi",
                                    "deplocation" : {
                                        "lat" : self.deplocation[0],
                                        "lon" : self.deplocation[1]
                                    }}
                             }, 
                             { "geo_distance" : {
                                    "distance" : "20mi",
                                    "arrlocation" : {
                                        "lat" : self.arrlocation[0],
                                        "lon" : self.arrlocation[1]
                                    }}
                                }
                          ]
                        }
                    }        
                }
              }
        }
    
        print "-----------Searching for nearby driver/rider-----------"
        res = self.client.search(query, index=self.index, doc_type=self.type)    
        hits = res['hits']['hits']
    
        # no nearby driver available
        if len(hits) == 0:
            print "No Drivers/Riders Found"
            return (1)
    
        print "Found %d drivers/riders" % len(hits)
        print json.dumps(hits)
        mid=[]
        deplat=[]
        deplon=[]
        arrlat=[]
        arrlon=[]        
        dist=[]
        for re in hits:
            mid.append(re['_source']['messageid'])
            deplat.append(re['_source']['deplocation']['lat'])
            deplon.append(re['_source']['deplocation']['lon'])
            arrlat.append(re['_source']['arrlocation']['lat'])
            arrlon.append(re['_source']['arrlocation']['lon'])            
            dist.append(re['sort'])
        return (deplat, deplon, arrlat, arrlon, dist, mid)
        