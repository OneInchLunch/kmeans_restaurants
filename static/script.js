document.addEventListener("DOMContentLoaded", function () {
    const resultList = document.getElementById('apiResult');
    const form = document.querySelector('form');

    // Since the dataset I found is of restaurants 
    // in Mexico, I randomly picked this as the
    // initial position of the user
    const initialPos = [22.154329, -100.987229];
    var userMarker = null;

    // The library used to display the map is leaflet
    // https://leafletjs.com/
    var mymap = L.map('map').setView(initialPos, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(mymap);

    // This function is used to create a new marker
    // and update the user's coordinates every time
    // the map is clicked.
    function onMapClick(e) {
        var clickedLatLng = e.latlng;
    
        if (userMarker) {
            mymap.removeLayer(userMarker);
        }
    
        var newMarker = L.marker(clickedLatLng).addTo(mymap);
    
        userMarker = newMarker;
        newMarker.bindPopup('Your Location')
        console.log(userMarker)
        
        f_lat = document.getElementById('latitude')
        f_lng = document.getElementById('longitude')

        f_lat.value = userMarker._latlng.lat
        f_lng.value = userMarker._latlng.lng
        
    }
    mymap.on('click', onMapClick)

    var markersLayer = L.layerGroup().addTo(mymap);

    function clearMarkers() {
        markersLayer.clearLayers();
    }

    //==========================================================
    // An attempt was made to have marker names
    // displayed on hover, but I got annoyed
    // and quit.
    // function onMarkerMouseover(e) {
    //     var marker = e.target;
    //     if (marker instanceof L.marker) {
    //         marker_name = marker._popup._content
    //         marker.bindPopup(marker_name).openPopup();
    //     }
    // }
    
    // function onMarkerMouseout(e) {
    //     var marker = e.traget;
    //     if (marker instanceof L.marker) {
    //         marker.closePopup();
    //     }
    // }

    // mymap.on('mouseover', onMarkerMouseover);
    // mymap.on('mouseout', onMarkerMouseout);
    //==========================================================

    
    // Function to update the UI with new data
    // This is called after every time the user 
    // sends new data for the k-means algorithm to
    // process.
    // This handles generating the new list
    // as well as creating new map markers.
    function updateUI(data) {
        resultList.innerHTML = ''; 
        
        data.restaurants.forEach(restaurant => {
        
            dist = Math.round(restaurant.Distance * 100)
            dist >= 1000 ? dist = `${dist / 100} km` : dist = `${dist} m`
    
            const listItem = document.createElement('li');

            listItem.innerHTML = `
                <strong>Name:</strong> ${restaurant.name}<br>
                <strong>Cuisine:</strong> ${restaurant.Rcuisine}<br>
                <strong>Rating:</strong> ${restaurant.rating}/5<br>
                <strong>Distance:</strong> ${dist}<br>
            `;

            resultList.appendChild(listItem);

            var marker = L.marker([restaurant.latitude, restaurant.longitude]);       
          
            marker.bindPopup(restaurant.name)
            markersLayer.addLayer(marker)


        });

    }

    // This is where the data is sent, please note
    // this is an API in concept only, basically
    // the only thing this so called "API" does is
    // recieve user data and sends it back
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        fetch('/api/submit_form', {
            method: 'POST',
            body: new FormData(form),
        })
        .then(response => response.json())
        .then(data => {
            clearMarkers();
            updateUI(data)
        })
        .catch(error => {
            console.error('Error submitting form:', error);
        });
    });

    // This endpoint is literally just used to populate
    // the frontend with some initial data.
    fetch('/api')
        .then(response => response.json())
        .then(data => {
            updateUI(data);
        })
        .catch(error => {
            console.error('Error fetching initial data:', error);
        });

});