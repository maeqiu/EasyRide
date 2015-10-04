// Render the matched driver/rider locations on Google Maps
var myLatlng = {lat: 37.5, lng: -121.0};
var markers = [];
var map;

function initialize(values) {
	markers = values;
	var myOptions = {
        zoom: 8,
        center: myLatlng
    };
    map = new google.maps.Map(document.getElementById("map"),
            myOptions);
	var bounds = new google.maps.LatLngBounds();
    showMatch(markers, map);
	document.getElementById("markers").click();
}

function showMatch(markers, map) {
	var len = 0;
    try {
    	len = markers.length;
	}
	catch(err){
		//alert('in markers.length error');
	}
	if(len > 0) {
		for (var index = 0; index < len-1;index++) {
			var character = index + 1
			var marker_text_color = "FFFFFF";
			var marker_color = "EE0024";   //red
			var marker = new google.maps.Marker({
				position: {lat: markers[index]['deplat'], lng: markers[index]['deplon']},
				map: map,
				icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color,
				title: String(markers[index]['distance'][0]) + ' km',
				messageid: markers[index]['messageid'],
				phone: markers[index]['phone']
			});
			google.maps.event.addListener(marker, 'click', function() {
				alert(index+','+this.phone);
				updateDatabase(this.messageid,this.phone,markers[len-1]['deplat'], markers[len-1]['deplon']);
			});
		
			var marker_color = "009BEE";   //blue
			var marker = new google.maps.Marker({
				position: {lat: markers[index]['arrlat'], lng: markers[index]['arrlon']},
				map: map,
				icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=" + character + "|" + marker_color + "|" + marker_text_color,
				title: String(markers[index]['distance'][1]) + ' km',
				messageid: markers[index]['messageid'],
				phone: markers[index]['phone']
			});
		
			google.maps.event.addListener(marker, 'click', function() {
				updateDatabase(this.messageid,this.phone,markers[len-1]['deplat'], markers[len-1]['deplon']);
			});
		}

		var marker = new google.maps.Marker({
			position: {lat: markers[len-1]['deplat'], lng: markers[markers.length-1]['deplon']},
			map: map,
			icon: 'http://maps.google.com/mapfiles/marker_purple.png',
			title: 'Starting location'
		});
	                                   
		var marker = new google.maps.Marker({
			position: {lat: markers[len-1]['arrlat'], lng: markers[len-1]['arrlon']},
			map: map,
			icon: 'http://maps.google.com/mapfiles/marker_green.png',
			title: 'Destination'
		});
	}                                    
	
}

function updateDatabase(messageid, phone, lat, lon) {
	alert(messageid+','+lat+','+lon);
	window.location.href = "http://ec2-54-215-228-56.us-west-1.compute.amazonaws.com/update/"+messageid+"/"+phone+"/"+lat+"/"+lon;
}