// Render the markers for driver/rider locations on Google Maps
var myLatlng = {lat: 37.5, lng: -121.0};
var markerlist = [];
var map;

function initialize() {
	var myOptions = {
        zoom: 9,
        center: myLatlng
    };
    map = new google.maps.Map(document.getElementById("map"),
            myOptions);
	var bounds = new google.maps.LatLngBounds();

	showLocations();
}

function showLocations() {
	clearMarkers();				
    $.getJSON('/geosdriver',
    	function(data) {
			geosdriver=data.geosdriver;
			if(geosdriver.length > 0) {
				for (var index = 0; index < geosdriver.length;index++) {
					var character = index + 1
					var marker_text_color = "FFFFFF";
					var marker_color = "EE0024";   //red
					var icon = {
						url:  "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color, // url
						//scaledSize: new google.maps.Size(30, 50) // scaled size
						//origin: new google.maps.Point(0,0), // origin
						//anchor: new google.maps.Point(0, 0) // anchor
					};
					var marker = new google.maps.Marker({
						position: {lat: geosdriver[index]['deplat'], lng: geosdriver[index]['deplon']},
						map: map,
						icon: icon,
						title: 'driver ' + String(character) + ', departing from (' + geosdriver[index]['deplat'] + ', ' + geosdriver[index]['deplon'] + ')'
					});
				
					google.maps.event.addListener(marker, 'click', function() {
						updateTextDep(this.getPosition());
					});
					markerlist.push(marker);   //add marker to the list
					
					var marker_color = "F74DE1";   //pink					
					var icon = {
						url:  "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color, // url
						//scaledSize: new google.maps.Size(30, 50) // scaled size
						//origin: new google.maps.Point(0,0), // origin
						//anchor: new google.maps.Point(0, 0) // anchor
					};
					var marker = new google.maps.Marker({
						position: {lat: geosdriver[index]['arrlat'], lng: geosdriver[index]['arrlon']},
						map: map,
						icon: icon,
						title: 'driver ' + String(character) + ', arriving at (' + geosdriver[index]['arrlat'] + ', ' + geosdriver[index]['arrlon'] + ')'
					});
					google.maps.event.addListener(marker, 'click', function() {
						updateTextArr(this.getPosition());
					});
					
					markerlist.push(marker);   //add marker to the list					
				}
			} else {
				alert("No drivers in the database")
			}
	});
	$.getJSON('/geosrider',
    	function(data) {
			geosrider=data.geosrider;
			if(geosdriver.length > 0) {	
				for (var index = 0; index < geosrider.length;index++) {
					var character = index + 1
					var marker_text_color = "FFFFFF";
					var marker_color = "4506F8";   //dark blue
					var marker = new google.maps.Marker({
						position: {lat: geosrider[index]['deplat'], lng: geosrider[index]['deplon']},
						map: map,
						icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color,
						title: 'rider ' + String(character) + ', departing from (' + geosrider[index]['deplat'] + ', ' + geosrider[index]['deplon'] + ')',
						anchor: new google.maps.Point(17, 34),
						size: new google.maps.Size(100,80)
					});
					google.maps.event.addListener(marker, 'click', function() {
						updateTextDep(this.getPosition());
					});
					markerlist.push(marker);   //add marker to the list
					
					var marker_color = "009BEE";   //blue
					var marker = new google.maps.Marker({
						position: {lat: geosrider[index]['arrlat'], lng: geosrider[index]['arrlon']},
						map: map,
						icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color,
						title: 'rider ' + String(character) + ', arriving at (' + geosrider[index]['arrlat'] + ', ' + geosrider[index]['arrlon'] + ')'
					});
					google.maps.event.addListener(marker, 'click', function() {
						updateTextArr(this.getPosition());
					});
					
					markerlist.push(marker);   //add marker to the list					
				}
			} else {
				alert("No riders in the database")
			}
	});	
	
	window.setTimeout(function(){
        showLocations()
    }, 5000);

}

function updateTextDep(position) {
	document.getElementById("deplat").value = position.lat();
	document.getElementById("deplon").value = position.lng();
}

function updateTextArr(position) {
	document.getElementById("arrlat").value = position.lat();
	document.getElementById("arrlon").value = position.lng();
}

function clearMarkers() {
    for (var i = 0; i < markerlist.length; i++) {
        markerlist[i].setMap(null);
    }
    markerlist = [];
}
