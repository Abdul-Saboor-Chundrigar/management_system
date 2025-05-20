# attendance_tracking/urls.py
from django.urls import path
from . import views

app_name = 'attendance_tracking'

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendance_list'),
    path('check-in/', views.AttendanceCheckInView.as_view(), name='check_in'),
    path('check-out/', views.AttendanceCheckOutView.as_view(), name='check_out'),
    path('report/', views.AttendanceReportView.as_view(), name='attendance_report'),
]
