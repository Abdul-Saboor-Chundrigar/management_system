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

// Update every minute
setInterval(updateTimestamps, 60000);
updateTimestamps(); // Initial update
