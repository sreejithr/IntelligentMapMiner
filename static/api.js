var geocoder;
var map;
var should_proceed = true;
var request_count = 0;

function initialize() {
  geocoder = new google.maps.Geocoder();
}

function getAddresses() {
  if (should_proceed == true) {
    $.ajax({
      'url' : 'http://127.0.0.1:5000/coordinate',
      'type' : 'GET',
      'success' : function(data) {
        if (data != 'null') {
          setTimeout('getAddresses()', 3000);
          latlng = data.split(',');
          codeLatLng(latlng);
        }
      }
    });
  } else
    document.getElementById('status').innerHTML = "What do I do now?<br/>Mining has been stopped due to a OVER_QUERY_LIMIT error. I recommend you wait for a while to start again!"
}

function codeLatLng(latLngList) {
  var lat = parseFloat(latLngList[0]);
  var lng = parseFloat(latLngList[1]);
  var latlng = new google.maps.LatLng(lat, lng);

  geocoder.geocode({'latLng': latlng}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        results[0]['coordinate'] = latlng.toString();
        var address = results[0];
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5000/data", true);
        xhr.setRequestHeader("Content-type", "text/plain");
        xhr.send(JSON.stringify(address));
        request_count++;
        console.log(request_count + "th request");
        document.getElementById('address').innerHTML += "<li>" + results[0].formatted_address + "</li>"
      } else {
        console.log('No results found');
      }
    } else if (status == google.maps.GeocoderStatus.OVER_QUERY_LIMIT) {
      console.log('Geocoder failed due to: ' + status);
      should_proceed = false;
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);