from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserActivity

@login_required
def activity_dashboard(request):
    activities = UserActivity.objects.select_related('user').order_by('-timestamp')[:100]
    return render(request, 'user_activity/dashboard.html', {
        'activities': activities,
        'total_activities': UserActivity.objects.count()
    })
