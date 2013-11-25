var geocoder;
var map;
var infowindow = new google.maps.InfoWindow();
var marker;
function initialize() {
  geocoder = new google.maps.Geocoder();
}

function getAddresses(json_coordinates) {
  j=0;
  coordinates = json_coordinates['data'];
  oneByOne(coordinates[j]);
  // for(var i=0; i<10; i++) {
  //   try {
  //     status = geoCodeLatLng(coordinates[i][0], coordinates[i][1]);
  //     sleep(2000);
  //     // if (status == 1) {
  //     //   document.getElementById('address').innerHTML += "<li>Requerying</li>";
  //     //   status = geoCodeLatLng(coordinates[i][0], coordinates[i][1]);
  //     //   setTimeout(function() { geoCodeLatLng(coordinates[i][0], coordinates[i][1]) }, 2000);
  //   } catch(e) {}
  // }
}

function oneByOne(coordinate) {
  j=j+1;
  if (j<10) {
    geoCodeLatLng(coordinate[0], coordinate[1]);
    setTimeout(oneByOne(coordinates[j]), 5000);
  }
}

function geoCodeLatLng(lat, lng) {
  var latlng = new google.maps.LatLng(lat, lng);
  result_status = null;

  geocoder.geocode({'latLng': latlng}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        var address = results[0];
        //address['address_no_of_words'] = len(address.formatted_address.split(',')) 
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:5000/data", true);
        xhr.setRequestHeader("Content-type", "text/plain");
        xhr.send(JSON.stringify(address));
        document.getElementById('address').innerHTML += "<li>" + latlng.toString() + results[0].formatted_address + "</li>";
      } else { /* TODO: No results. Log these coordinates */
        document.getElementById('address').innerHTML += "<li>NO RESULT</li>";
      }
    } else if(status == "OVER_QUERY_LIMIT") {
        result_status = status;
    }
  });

  // if (result_status == "OVER_QUERY_LIMIT") {
  //   console.log(result_status);
  //   return 1
  // } else { return 0; }
}

google.maps.event.addDomListener(window, 'load', initialize);