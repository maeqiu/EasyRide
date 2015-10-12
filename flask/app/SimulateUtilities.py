'''
Created on Oct 1, 2015

@author: maeq
'''
import random
from MatchUtilities import matchRides
from UpdateUtilities import mark4deletionByLatLon 
from UpdateUtilities import updateByMessageid
from UpdateUtilities import updateByLatLon

class simulateUser(object):
    def __init__(self, es_client, esindex, estype, deploc, arrloc, drflag):
        self.client=es_client
        self.index = esindex
        self.type = estype
        self.deplocation = deploc
        self.arrlocation = arrloc
        self.drflag = drflag
            
    def simulating(self):
        producer = matchRides(self.client,self.index,self.type,self.deplocation,self.arrlocation,self.drflag)
        result = producer.matching()
        if (result != 1):    #found matching drivers/riders
            (deplats,deplons,arrlats,arrlons,dist,messageid,phone) = result
            
            #randomly pick up a user
            pickup=random.choice(range(len(deplats)))
            print "picking up driver/rider %d" % pickup
            
            requestingProducer = mark4deletionByLatLon(self.client, self.index, self.type, self.deplocation[0], self.deplocation[1])    
            markid = requestingProducer.marking()
            #if the requesting rider/driver is still available, check whether the requested driver/rider is available.
            if markid != 1:
                requestedProducer = updateByMessageid(self.client, self.index, self.type, messageid[pickup])    
                success = requestedProducer.updating()
                if success == 1:
                    print "The driver/rider isn't available anymore. Please select again!"
                else:
                    self.client.delete(self.index, self.type, markid)
                    print "Both driver and rider have been confirmed!"
                    
            else:
                print "You have been selected by other driver/rider."       
                
            
