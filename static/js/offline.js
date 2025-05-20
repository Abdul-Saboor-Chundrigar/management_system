// Add to your offline.js
if (!navigator.onLine) {
    L.tileLayer('/path/to/local/tiles/{z}/{x}/{y}.png').addTo(map);
}
