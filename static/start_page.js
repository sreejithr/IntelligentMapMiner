var map;
var rectangle;
var rectangle_mode = false;

function calculate_coordinates_with_form_data(WEB_SERVER) {
	latlng = document.latlng_info.latlng.value;
	zoom_level = document.controls.zoom_level.value;
	action_url = WEB_SERVER + 'kickstart';
	$.ajax({
		type: "POST",
		url: action_url,
		data: {latlng: latlng, zoom_level: zoom_level},
		success: function(data, textStatus, jqXHR) {
			document.getElementById('status').innerHTML = "<p>What do I do now? -- Server has the coordinates, bro! Ready to 'Pull Data'</p>";
		}
 	});
}


function calculate_coordinates(WEB_SERVER) {
	has_coordinates = 'true';
	try {
		bounds = rectangle.getBounds();
		sw = bounds.getSouthWest().lat() + ',' + bounds.getSouthWest().lng();
		ne = bounds.getNorthEast().lat() + ',' + bounds.getNorthEast().lng();
	} catch (e) { //if e instanceof TypeError) {
		has_coordinates = 'false';
		sw = 0;
		ne = 0;
	}
	zoom_level = document.controls.zoom_level.value;
	action_url = WEB_SERVER + 'kickstart';

	$.ajax({
		type: "POST",
		url: action_url,
		data: {has_coordinates: has_coordinates, sw: sw, ne: ne, zoom_level: zoom_level},
		success: function(data, textStatus, jqXHR) {
			console.log(data);
			document.getElementById('status').innerHTML = "<p>What do I do now? -- Server has the coordinates, bro! Ready to 'Pull Data'</p>";
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
	initial = new google.maps.LatLng(17.3660, 78.4760);
	map_options = {
		zoom: 10,
		center: initial
	};
	map = new google.maps.Map(document.getElementById('map'), map_options);
	document.getElementById('status').innerHTML = "<p>What do I do now? <br/>Try 'Pull Data'. If not working, select an area, zoom level and 'Calculate Coordinates'</p>";
}


google.maps.event.addDomListener(window, 'load', initialize);