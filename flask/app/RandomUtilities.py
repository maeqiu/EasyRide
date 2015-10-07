'''
Created on Sep 14, 2015

@author: maeq
'''
import json
import random
import os
import datetime
import time
import math
from faker import Factory

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y,%m,%d,%H,%M,%S', prop)

def randomLatLon(lat, lon, radius, num_rows):
    """ generate random Lat Long positions within radium(meters) from (lat,lon)
    number of Lat Long to be generated equals num_rows
    """
    radiusInDegrees=radius/111300.           
    r = radiusInDegrees
    x0 = lat
    y0 = lon
    latlist=[]
    lonlist=[]
    
    for _ in range(num_rows):
    
        u = float(random.uniform(0.0,1.0))
        v = float(random.uniform(0.0,1.0))
        
        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t) 
        y = w * math.sin(t)
          
        xLat  = x + x0
        yLong = y + y0
        latlist.append(xLat)
        lonlist.append(yLong)
        
    return latlist, lonlist

def randomSingleLatLon(lat, lon, radius):
    """ generate a single random pair of Lat Long position within radium(meters) from (lat,lon)
    """
    radiusInDegrees=radius/111300.           
    r = radiusInDegrees
    x0 = lat
    y0 = lon
   
    u = float(random.uniform(0.0,1.0))
    v = float(random.uniform(0.0,1.0))
    
    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t) 
    y = w * math.sin(t)
      
    xLat  = x + x0
    yLong = y + y0
        
    return xLat, yLong

def create_json_message(phone, latdep, longdep, latarr, longarr, timestamp, dr_flag, user_id, message_id):
    """Create JSON messages with different message fields
    
    Args:
        phone: a person's phone number, string
        latdep: departing latitude, double
        longdep: departing longitude, double
        latarr: arriving latitude, double
        longarr: arriving longitude, double
        timestamp: the timestamp when the message was sent in the format of
                  "year, month, day, hour, minute, second", string
        dr_flag: flag indicating it's driver or rider (1 for driver, 0 for rider), integer
        user_id: user ID, integer
        
    Returns:
        A string in JSON format
        example:
        {'phone': "1-541-123-4567",
         'latdep': 37.426327,
         'longdep': -122.141076,
         "longarr": -121.650043, 
         "latarr": 38.142658,
         'timestamp': "2015, 2, 8, 12, 13, 49",
         'dr_flag': 1,
         'user_id': 00001}
    """
    message_info = {"phone": phone,
                    "latdep": latdep,
                    "longdep": longdep,
                    "latarr": latarr,
                    "longarr": longarr,
                    "timestamp": timestamp,
                    "drFlag": dr_flag,
                    "userID": user_id,
                    "messageID": message_id}

    return json.dumps(message_info)
