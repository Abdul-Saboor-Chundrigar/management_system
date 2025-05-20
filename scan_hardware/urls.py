from django.urls import path
from . import views

app_name = 'scan_hardware'

urlpatterns = [
    path('scan/', views.scan_machine, name='scan'),
]
