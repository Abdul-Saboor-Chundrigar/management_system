from django.urls import path
from . import views

app_name = 'warehouse_management'

urlpatterns = [
    path('', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('add/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('<int:pk>/edit/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('<int:pk>/delete/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),
]
