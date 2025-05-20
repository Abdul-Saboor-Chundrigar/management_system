// Initialize map
const map = L.map('map').setView([24.8607, 67.0011], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add markers for each location
document.querySelectorAll('tbody tr').forEach(row => {
    const lat = parseFloat(row.dataset.lat || 0);
    const lng = parseFloat(row.dataset.lng || 0);
    
    if (lat && lng) {
        const marker = L.marker([lat, lng]).addTo(map)
            .bindPopup(`
                <b>${row.cells[0].innerText}</b><br>
                ${row.cells[1].querySelector('strong').innerText}<br>
                <small>${row.cells[1].querySelector('small').innerText}</small>
            `);
        
        // Center map when view button clicked
        row.querySelector('.view-btn').addEventListener('click', () => {
            map.setView([lat, lng], 15);
            marker.openPopup();
        });
    }
});

// Auto-update timestamps
function updateTimestamps() {
    document.querySelectorAll('.time-ago').forEach(el => {
        const timestamp = new Date(el.dataset.timestamp);
        el.textContent = formatTimeAgo(timestamp);
    });
}

function formatTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };
    
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval === 1 ? '' : 's'} ago`;
        }
    }
    return 'just now';
}

setInterval(updateTimestamps, 60000);
updateTimestamps();
document.addEventListener('DOMContentLoaded', function() {
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Update location
    const updateLocation = debounce(function(latitude, longitude) {
        console.log('Coords:', latitude, longitude);
        fetch("{% url 'live:update_location' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: `latitude=${latitude}&longitude=${longitude}`
        }).then(response => response.json()).then(data => {
            if (data.status === 'error') {
                console.error('Update error:', data.message);
            }
        }).catch(() => {});
    }, 300000); // Update every 5 minutes

    // Trigger geolocation only on /live/monitor/
    if (navigator.geolocation && {{ request.user.is_authenticated|lower }} && window.location.pathname === '/live/monitor/') {
        navigator.geolocation.getCurrentPosition(
            position => {
                updateLocation(position.coords.latitude, position.coords.longitude);
            },
            error => console.error('Geolocation error:', error),
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
        );

        // Watch for position changes
        navigator.geolocation.watchPosition(
            position => {
                updateLocation(position.coords.latitude, position.coords.longitude);
            },
            error => console.error('Geolocation error:', error),
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
        );
    }
});

<script>
// Add this to your JavaScript
$('#cleanup-btn').click(function() {
    if (confirm('Delete all location records older than 30 days?')) {
        $.ajax({
            url: '{% url "live:cleanup_locations" %}',
            method: 'POST',
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            success: () => {
                alert('Cleanup completed!');
                location.reload();
            }
        });
    }
});
</script>
