import json
import random
import sys
import time

from pyelasticsearch import ElasticSearch

class matchRides(object):
    def __init__(self, esindex, deploc, arrloc, drflag):
        self.esindex = esindex
        self.deplocation = deploc
        self.arrlocation = arrloc
        self.drflag = drflag
            
    def matching(self):
        es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
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
    
        print "-----------executing search query-----------"
        res = es_client.search(query, index=self.esindex)    
        hits = res['hits']['hits']        
    
        # no nearby driver available
        if len(hits) == 0:
            print "No Drivers Found"
            return (1)
    
        print "Found %d drivers" % len(hits)
        print json.dumps(hits)
        mid=[]
        deplat=[]
        deplon=[]
        arrlat=[]
        arrlon=[]        
        dist=[]
        for re in hits:
            name = re['_source']['name']
            mid.append(re['_source']['messageid'])
            deplat.append(re['_source']['deplocation']['lat'])
            deplon.append(re['_source']['deplocation']['lon'])
            arrlat.append(re['_source']['arrlocation']['lat'])
            arrlon.append(re['_source']['arrlocation']['lon'])            
            dist.append(re['sort'])
        return (deplat, deplon, arrlat, arrlon, dist, mid)
        