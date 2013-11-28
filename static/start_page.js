var map;
var rectangle_mode = false;

function kickstart() {
	latlng = document.latlng_info.latlng.value;
	zoom_level = document.latlng_info.zoom_level.value;
	action_url = 'http://127.0.0.1:5000/kickstart'
	$.ajax({
		type: "POST",
		url: action_url,
		data: {latlng: latlng, zoom_level: zoom_level},
		success: function(data, textStatus, jqXHR) {
			document.getElementById('coordinates').innerHTML = "<p>Status: " + data + "</p>";
		}
 	});
}

function toggle_rectangle_mode() {
	rectangle = new google.maps.Rectangle({
		editable: true,
		draggable: true,
		map: map,
		bounds: map.getBounds()
	})
}

function initialize() {
	initial = new google.maps.LatLng(18.5204303, 73.85674369999992);
	map_options = {
		zoom: 5,
		center: initial
	};
	map = new google.maps.Map(document.getElementById('map'), map_options);
}



google.maps.event.addDomListener(window, 'load', initialize);