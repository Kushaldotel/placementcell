 /*========== leaflet map=======*/
    var map = L.map('map', {
        scrollWheelZoom: false
    }).setView([23.8959, 89.1348], 15);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    L.marker([23.8959, 89.1348], {icon: customMarker}).addTo(map).bindPopup('This is your.<br> Company Location.').openPopup();
    var customMarker = L.icon({
        iconUrl: './../img/icon/map-marker.png',
        iconSize: [58, 95],
        iconAnchor: [29, 94],
        popupAnchor: [17, -34],
    });