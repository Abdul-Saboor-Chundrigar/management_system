from django.urls import path
from . import views

app_name = 'user_activity'

urlpatterns = [
    path('', views.activity_dashboard, name='activity_dashboard'),
]
