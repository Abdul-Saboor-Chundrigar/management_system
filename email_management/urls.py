from django.urls import path
from . import views

app_name = 'email_management'

urlpatterns = [
    path('send/', views.send_emails, name='send_emails'),
    path('logs/', views.email_log_list, name='email_log_list'),
    path('logs/delete/<int:id>/', views.delete_email_log, name='delete_email_log'),
]
