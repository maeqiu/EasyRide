// Render the markers for driver/rider locations on Google Maps
var myLatlng = {lat: 36.9, lng: -120.51};
var markers = [];
var map;

function initialize() {
	var myOptions = {
        zoom: 8,
        center: myLatlng
    };
    map = new google.maps.Map(document.getElementById("map"),
            myOptions);
	var bounds = new google.maps.LatLngBounds();
	showLocations(map);
}

function showLocations(map) {
    $.getJSON('/geosdriver',
    	function(data) {
			geosdriver=data.geosdriver;			
			
			for (var index = 0; index < geosdriver.length;index++) {
				var character = index + 1
				var marker_text_color = "FFFFFF";
				var marker_color = "EE0024";   //red
				var icon = {
					url:  "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color, // url
					scaledSize: new google.maps.Size(30, 50), // scaled size
					origin: new google.maps.Point(0,0), // origin
					anchor: new google.maps.Point(0, 0) // anchor
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
		
				var marker_color = "259311";   //green
				var icon = {
					url:  "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color, // url
					scaledSize: new google.maps.Size(30, 50), // scaled size
					origin: new google.maps.Point(0,0), // origin
					anchor: new google.maps.Point(0, 0) // anchor
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
			}
	});
	$.getJSON('/geosrider',
    	function(data) {
			geosrider=data.geosrider;
						
			for (var index = 0; index < geosrider.length;index++) {
				var character = index + 1
				var marker_text_color = "FFFFFF";
				//var marker_color = "6419EF";   //purple
				var marker_color = "AB2FDE";   //another purple
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
			}
	});	
}

function updateTextDep(position) {
	document.getElementById("deplat").value = position.lat();
	document.getElementById("deplon").value = position.lng();
}

function updateTextArr(position) {
	document.getElementById("arrlat").value = position.lat();
	document.getElementById("arrlon").value = position.lng();
}