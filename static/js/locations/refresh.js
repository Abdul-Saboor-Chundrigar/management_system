document.getElementById('refresh-btn').addEventListener('click', function() {
    fetch(REFRESH_URL, {  // Use the variable here
        method: 'POST',
        headers: { 
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    }).then(response => location.reload());
});
