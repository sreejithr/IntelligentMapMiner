var geocoder;
var map;
var should_proceed = true;
var request_count = 0;
var last_unprocessed_coordinate = [];
var server_url;

function initialize() {
  geocoder = new google.maps.Geocoder();
}

function getAddresses(WEB_SERVER) {
  server_url = WEB_SERVER;
  if (last_unprocessed_coordinate.length > 0)
    codeLatLng(last_unprocessed_coordinate.pop());

  if (should_proceed == true) {
    $.ajax({
      'url' : server_url + 'coordinate',
      'type' : 'GET',
      'success' : function(data) {
        if (data != 'null') {
          setTimeout('getAddresses('+action_url+')', 3000);
          latlng = data.split(',');
          codeLatLng(latlng);
        }
      }
    });
  } else
    document.getElementById('status').innerHTML = "What do I do now?<br/>Mining has been stopped due to a OVER_QUERY_LIMIT error. I recommend you wait for a while to start again!";
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
        xhr.open("POST", server_url + "data", true);
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
      last_unprocessed_coordinate.push(latLngList);
      should_proceed = false;
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);