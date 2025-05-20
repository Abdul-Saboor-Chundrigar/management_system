from django.urls import path
from . import views

app_name = 'custom_email_client'

urlpatterns = [
    path('', views.email_list, name='email_list'),
    path('send/', views.send_email, name='send_email'),
    path('receive/', views.receive_emails, name='receive_emails'),
    path('test/', views.test_email, name='test_email'),
]
