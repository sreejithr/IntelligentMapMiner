var geocoder;
var map;
var infowindow = new google.maps.InfoWindow();
var marker;
function initialize() {
  geocoder = new google.maps.Geocoder();
}

function getAddresses(json_coordinates) {
  coordinates = json_coordinates['data'];
  for(var i=0; i<10; i++) {
    try {
      geoCodeLatLng(coordinates[i][0], coordinates[i][1]);
    } catch(e) {}
  }
}

function geoCodeLatLng(lat, lng) {
  var latlng = new google.maps.LatLng(lat, lng);

  geocoder.geocode({'latLng': latlng}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        var address = results[0];
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5000/data", true);
        xhr.setRequestHeader("Content-type", "text/plain");
        xhr.send(JSON.stringify(address))
        document.getElementById('address').innerHTML += "<li>" + results[1].formatted_address + "</li>"
      } else {
        alert('No results found');
      }
    } else {
      alert('Geocoder failed due to: ' + status);
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);