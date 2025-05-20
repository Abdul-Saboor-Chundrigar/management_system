from django.urls import path
from . import views

app_name = 'posteio_integration'

urlpatterns = [
    path('configure/', views.configure_posteio, name='configure_posteio'),
]
