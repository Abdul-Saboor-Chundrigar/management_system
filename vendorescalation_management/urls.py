from django.urls import path
from . import views

app_name = 'vendorescalation_management'

urlpatterns = [
    path('', views.VendorEscalationManagementListView.as_view(), name='vendor_list'),
    path('add/', views.VendorEscalationManagementCreateView.as_view(), name='vendor_create'),
    path('<int:pk>/', views.VendorEscalationManagementDetailView.as_view(), name='vendor_detail'),
    path('<int:pk>/edit/', views.VendorEscalationManagementUpdateView.as_view(), name='vendor_update'),
    path('<int:pk>/delete/', views.VendorEscalationManagementDeleteView.as_view(), name='vendor_delete'),
]
