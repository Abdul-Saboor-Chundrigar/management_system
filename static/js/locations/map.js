// Initialize map with better controls
const map = L.map('map', {
    zoomControl: false
}).setView([24.8607, 67.0011], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

// Add custom zoom control
L.control.zoom({
    position: 'topright'
}).addTo(map);

// Add markers with custom icons
const userIcon = L.icon({
    iconUrl: '/static/images/user-marker.png',
    iconSize: [32, 32],
    popupAnchor: [0, -15]
});

// Process locations
document.querySelectorAll('tbody tr').forEach(row => {
    const lat = parseFloat(row.dataset.lat || 0);
    const lng = parseFloat(row.dataset.lng || 0);
    
    if (lat && lng) {
        const marker = L.marker([lat, lng], {icon: userIcon}).addTo(map)
            .bindPopup(row.cells[0].innerText);
        
        row.addEventListener('mouseenter', () => marker.openPopup());
        row.addEventListener('mouseleave', () => marker.closePopup());
    }
});
