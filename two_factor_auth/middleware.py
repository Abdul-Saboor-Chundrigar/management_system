from django.shortcuts import redirect
from django.urls import reverse
from .models import UserTwoFactor

class TwoFactorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.path.startswith('/two_factor_auth/'):
                two_factor = UserTwoFactor.objects.filter(user=request.user).first()
                if two_factor and not two_factor.is_verified:
                    return redirect(reverse('verify_2fa'))
        
        return self.get_response(request)

def __call__(self, request):
    if request.user.is_authenticated and not request.user.is_staff:
        exempt_paths = ['/2fa/', '/logout/']  # Add paths to exclude
        if not any(request.path.startswith(path) for path in exempt_paths):
            two_factor = UserTwoFactor.objects.filter(user=request.user).first()
            if not two_factor or not two_factor.is_verified:
                return redirect(reverse('verify_2fa'))
    return self.get_response(request)
