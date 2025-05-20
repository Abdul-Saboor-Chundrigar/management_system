document.addEventListener('DOMContentLoaded', function() {
    const trackActivity = (activityType, data = {}) => {
        fetch('/user-activity/track/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                activity_type: activityType,
                url: window.location.pathname,
                data: data
            })
        });
    };

    // Track page views
    trackActivity('page_view', {
        referrer: document.referrer,
        screen_resolution: `${window.screen.width}x${window.screen.height}`
    });

    // Track interactions (example)
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            trackActivity('link_click', {
                href: e.target.href,
                text: e.target.innerText
            });
        }
    });
});
