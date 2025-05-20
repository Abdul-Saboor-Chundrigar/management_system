from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivity

@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        activity_type='login',
        url=request.path,
        details={
            'method': 'form',
            'user_agent': request.META.get('HTTP_USER_AGENT', '')
        }
    )

@receiver(user_logged_out)
def track_logout(sender, request, user, **kwargs):
    UserActivity.objects.create(
        user=user,
        activity_type='logout',
        url=request.path,
        details={
            'session_duration': (timezone.now() - request.user.last_login).total_seconds() 
            if hasattr(request.user, 'last_login') else None
        }
    )
