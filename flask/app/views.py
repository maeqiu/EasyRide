from app import app
from MatchUtilities import matchRides 
from RetrieveUtilities import retrieveLocations 
from UpdateUtilities import updateByMessageid
from UpdateUtilities import mark4deletionByLatLon
from UpdateUtilities import updateByLatLon
import UpdateUtilities as uutil
from flask import Flask, render_template, redirect, url_for, request, jsonify, json
from pyelasticsearch import ElasticSearch

@app.route("/")
@app.route("/locations")
def locations():
    return render_template('map_locations.html')

# link to the slides
@app.route("/slides")
def slides():
    return render_template("slides.html")

@app.route("/entry")
def entry():
    return render_template("request_form.html")

@app.route("/entry_results", methods=['POST'])
def entry_results():
    deplat = float(request.form['deplat'])
    deplon = float(request.form['deplon'])
    arrlat = float(request.form['arrlat'])
    arrlon = float(request.form['arrlon'])
    drflag = int(request.form['drflag'])

    es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
    producer = matchRides(es_client,'messages','myMessages',[deplat,deplon],[arrlat,arrlon],drflag)
    result = producer.matching()
    print "----------------------"
    geosmatch=[]
    if (result != 1):    #found matching driver/rider 
        (deplats,deplons,arrlats,arrlons,dist,mid,phone) = result
        geosmatch = [{"messageid": mid[ind], "phone": str(phone[ind]), "deplat": deplats[ind], "deplon": deplons[ind], "arrlat": arrlats[ind], "arrlon": arrlons[ind], "distance": dist[ind]} for ind in range(len(deplats))]
        geosmatch.append({"messageid": 0, "phone": '1-000-000-0000', "deplat": deplat, "deplon": deplon, "arrlat": arrlat, "arrlon": arrlon, "distance": [0,0]})
        print geosmatch
        return render_template('map.html',geosmatch=geosmatch)
    else:
        return render_template("confirm.html", message = "Sorry, no nearby drivers/riders available")

@app.route("/geosdriver")
def geosdriver():
    drflag = 1
    es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
    producer = retrieveLocations(es_client, 'messages', 'myMessages', drflag)    
    deplats,deplons,arrlats,arrlons = producer.retrieving()
    
    geosdriver = [{"deplat": deplats[ind], "deplon": deplons[ind], "arrlat": arrlats[ind], "arrlon": arrlons[ind]} for ind in range(len(deplats))]
    return jsonify(geosdriver=geosdriver)

@app.route("/geosrider")
def geosrider():
    drflag = 0
    es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
    producer = retrieveLocations(es_client, 'messages', 'myMessages', drflag)
    deplats,deplons,arrlats,arrlons = producer.retrieving()
    
    geosrider = [{"deplat": deplats[ind], "deplon": deplons[ind], "arrlat": arrlats[ind], "arrlon": arrlons[ind]} for ind in range(len(deplats))]
    return jsonify(geosrider=geosrider)

@app.route("/update/<messageid>/<phone>/<lat>/<lon>")
def updateWithPhone(messageid,phone,lat,lon):
    es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
    producer1 = mark4deletionByLatLon(es_client, 'messages', 'myMessages', lat, lon)    
    markid = producer1.marking()
    #if the rider/driver is still available, remove the corresponding initiating driver/rider and confirm.
    if markid != 1:
        producer2 = updateByMessageid(es_client, 'messages', 'myMessages', messageid)    
        success = producer2.updating()
        if success == 1:
            message = "You have been selected by other driver/rider."
        else:
            es_client.delete('messages', 'myMessages', markid)
            message = "Both driver and rider have been confirmed! Please contact " + phone
            
    else:       
        message = "The driver/rider isn't available anymore. Please select again!"
        
    return render_template("confirm.html", message = message)
  
@app.route("/update/<messageid>/<lat>/<lon>")
def updateLatLon(messageid,lat,lon):
    es_client = ElasticSearch("http://ec2-54-219-169-37.us-west-1.compute.amazonaws.com:9200")
    producer1 = mark4deletionByLatLon(es_client, 'messages', 'myMessages', lat, lon)    
    markid = producer1.marking()
    #if the rider/driver is still available, remove the corresponding initiating driver/rider and confirm.
    if markid != 1:
        producer2 = updateByMessageid(es_client, 'messages', 'myMessages', messageid)    
        success = producer2.updating()
        if success == 1:
            message = "You have been selected by other driver/rider."
        else:
            es_client.delete('messages', 'myMessages', markid)
            message = "Both driver and rider have been confirmed!"
            
    else:       
        message = "The driver/rider isn't available anymore. Please select again!"
        
    return render_template("confirm.html", message = message)

    