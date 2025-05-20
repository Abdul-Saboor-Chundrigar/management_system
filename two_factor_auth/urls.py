from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.setup_2fa, name='setup_2fa'),
    path('verify/', views.verify_2fa, name='verify_2fa'),
    path('login/', views.TwoFactorLoginView.as_view(), name='two_factor_login'),
]
