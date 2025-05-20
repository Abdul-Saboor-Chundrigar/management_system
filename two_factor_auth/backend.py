from django.contrib.auth.backends import ModelBackend
from .models import UserTwoFactor

class TwoFactorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user:
            if not UserTwoFactor.objects.filter(user=user).exists():
                return user
            if request.session.get('2fa_verified'):
                return user
        return None
