from django.urls import path
from . import views

app_name = 'file_attachment'

urlpatterns = [
    path('', views.attachment_list, name='attachment_list'),
    path('add/<str:emp_number>/', views.add_attachment, name='add_attachment'),
    path('edit/<int:id>/', views.edit_attachment, name='edit_attachment'),
    path('download/<int:id>/', views.download_attachment, name='download_attachment'),
    path('delete/<int:id>/', views.delete_attachment, name='delete_attachment'),
]
