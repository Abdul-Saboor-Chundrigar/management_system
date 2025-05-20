from django.urls import path
from . import views

app_name = 'live'

urlpatterns = [
    path('monitor/', views.admin_location_monitor, name='admin_location_monitor'),
    path('refresh/', views.refresh_locations, name='refresh_locations'),
    path('delete/<int:pk>/', views.delete_location, name='delete_location'),

    path('export/', views.export_locations, name='export_locations'),  # Main export URL
    path('export/csv/', views.export_locations, {'format': 'csv'}, name='export_csv'),
    path('export/pdf/', views.export_locations, {'format': 'pdf'}, name='export_pdf'),
    path('export/doc/', views.export_locations, {'format': 'doc'}, name='export_doc'),
    
    path('cleanup/', views.cleanup_locations, name='cleanup_locations'),
    path('update/', views.update_location, name='update_location'),
]
