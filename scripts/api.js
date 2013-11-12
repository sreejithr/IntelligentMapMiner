var geocoder;
var map;
var infowindow = new google.maps.InfoWindow();
var marker;
function initialize() {
  geocoder = new google.maps.Geocoder();
}

function getAddresses() {
  for(var i=0; i<10; i++) {
    codeLatLng(latlng[i][0], latlng[i][1]);
    console.log(i);
  }
}

function codeLatLng(lat, lng) {
  // var input = document.getElementById('latlng').value;
  // var latlngStr = input.split(',', 2);
  // var lat = parseFloat(latlngStr[0]);
  // var lng = parseFloat(latlngStr[1]);
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