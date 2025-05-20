from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import login as otp_login
from .models import UserTwoFactor
import qrcode
import base64
from io import BytesIO

def setup_2fa(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    device, created = TOTPDevice.objects.get_or_create(user=request.user, name='default')
    if created:
        device.save()
    
    # Generate QR code
    config_url = device.config_url
    img = qrcode.make(config_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'two_factor_auth/setup.html', {
        'qr_code': qr_code,
        'secret_key': device.key
    })

def verify_2fa(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        device = TOTPDevice.objects.get(user=request.user)
        
        if device.verify_token(token):
            UserTwoFactor.objects.update_or_create(
                user=request.user,
                defaults={'is_verified': True}
            )
            otp_login(request, device)
            return redirect('home')
    
    return render(request, 'two_factor_auth/verify.html')

class TwoFactorLoginView(LoginView):
    template_name = 'two_factor_auth/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if UserTwoFactor.objects.filter(user=user, is_verified=True).exists():
            self.request.session['user_id_for_2fa'] = user.id
            return redirect('verify_2fa')
        return super().form_valid(form)


from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_otp.plugins.otp_totp.models import TOTPDevice

class CustomLoginView(LoginView):
    def done(self, form_list, **kwargs):
        response = super().done(form_list, **kwargs)
        user = self.request.user
        
        # Skip 2FA for administrator
        if user.username == 'administrator':
            return response
        
        # Check if user has a verified TOTP device
        has_2fa = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
        
        # Redirect to 2FA setup if no verified device
        if not has_2fa:
            return redirect(reverse_lazy('two_factor:setup'))
        
        return response
