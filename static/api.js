var geocoder;
var map;
var infowindow = new google.maps.InfoWindow();
var marker;
var maxLimit = 0;

function initialize() {
  geocoder = new google.maps.Geocoder();
}

function getAddresses() {
    $.ajax({
      'url' : 'http://127.0.0.1:5000/coordinate',
      'type' : 'GET',
      'success' : function(data) {
        if (data != 'null') {
          setTimeout('getAddresses()', 2000);
          latlng = data.split(',');
          codeLatLng(latlng);
        }
      }
    });
}

function codeLatLng(latLngList) {
  var lat = parseFloat(latLngList[0]);
  var lng = parseFloat(latLngList[1]);
  var latlng = new google.maps.LatLng(lat, lng);

  geocoder.geocode({'latLng': latlng}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        var address = results[0];
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5000/data", true);
        xhr.setRequestHeader("Content-type", "text/plain");
        xhr.send(JSON.stringify(address))
        document.getElementById('address').innerHTML += "<li>" + results[0].formatted_address + "</li>"
      } else {
        console.log('No results found');
      }
    } else {
      console.log('Geocoder failed due to: ' + status);
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);