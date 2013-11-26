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