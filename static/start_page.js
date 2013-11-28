var map;
var rectangle;
var rectangle_mode = false;

function calculate_coordinates_with_form_data() {
	latlng = document.latlng_info.latlng.value;
	zoom_level = document.latlng_info.form_zoom_level.value;
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


function calculate_coordinates() {
	bounds = rectangle.getBounds();
	zoom_level = document.controls.zoom_level.value;

	sw = bounds.getSouthWest().lat() + ',' + bounds.getSouthWest().lng();
	ne = bounds.getNorthEast().lat() + ',' + bounds.getNorthEast().lng();

	action_url = 'http://127.0.0.1:5000/kickstart'
	$.ajax({
		type: "POST",
		url: action_url,
		data: {sw: sw, ne: ne, zoom_level: zoom_level},
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
	});
}


function initialize() {
	initial = new google.maps.LatLng(18.5204303, 73.85674369999992);
	map_options = {
		zoom: 15,
		center: initial
	};
	map = new google.maps.Map(document.getElementById('map'), map_options);
}


google.maps.event.addDomListener(window, 'load', initialize);