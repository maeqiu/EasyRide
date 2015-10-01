from app import app
from MatchUtilities import matchRides 
from RetrieveUtilities import retrieveLocations 
from UpdateUtilities import updateByMessageid
from UpdateUtilities import updateByLatLon
from flask import Flask, render_template, redirect, url_for, request, jsonify, json

@app.route("/entry")
def entry():
    return render_template("request_form.html")

@app.route('/entry_results', methods=['POST'])
def entry_results():
    deplat = float(request.form['deplat'])
    deplon = float(request.form['deplon'])
    arrlat = float(request.form['arrlat'])
    arrlon = float(request.form['arrlon'])
    if request.form.get('driver'):
        drflag=1
    if request.form.get('rider'):
        drflag=0
    producer = matchRides('test',[deplat,deplon],[arrlat,arrlon],drflag)
    
    mid,deplats,deplons,arrlats,arrlons,dist = producer.matching()
    geosmatch = [{"messageid": mid[ind], "deplat": deplats[ind], "deplon": deplons[ind], "arrlat": arrlats[ind], "arrlon": arrlons[ind], "distance": dist[ind]} for ind in range(len(deplats))]
    geosmatch.append({"messageid": 0,"deplat": deplat, "deplon": deplon, "arrlat": arrlat, "arrlon": arrlon, "distance": [0,0]})
    
    return render_template('map.html',geosmatch=geosmatch)

@app.route("/locations")
def locations():
    return render_template('map_locations.html')

@app.route("/geosdriver")
def geosdriver():
    drflag = 1
    producer = retrieveLocations('test', drflag)    
    deplats,deplons,arrlats,arrlons = producer.retrieving()
    
    geosdriver = [{"deplat": deplats[ind], "deplon": deplons[ind], "arrlat": arrlats[ind], "arrlon": arrlons[ind]} for ind in range(len(deplats))]
    return jsonify(geosdriver=geosdriver)

@app.route("/geosrider")
def geosrider():
    drflag = 0
    producer = retrieveLocations('test', drflag)    
    deplats,deplons,arrlats,arrlons = producer.retrieving()
    
    geosrider = [{"deplat": deplats[ind], "deplon": deplons[ind], "arrlat": arrlats[ind], "arrlon": arrlons[ind]} for ind in range(len(deplats))]
    return jsonify(geosrider=geosrider)

@app.route('/update/<messageid>')
def updateMessage(messageid):
    producer = updateByMessageid('test', 'myMessages', messageid)    
    producer.updating()
    return render_template('map_locations.html')
  
@app.route('/update/<messageid>/<lat>/<lon>')
def updateLatLon(messageid,lat,lon):
    producer1 = updateByMessageid('test', 'myMessages', messageid)    
    producer1.updating()
    producer2 = updateByLatLon('test', 'myMessages', lat, lon)    
    producer2.updating()
    return redirect('/locations')
  

    