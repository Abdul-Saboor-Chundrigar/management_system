from django.urls import path
from report_generation.views import ReportView
from .import views 

app_name = 'report_generation'

urlpatterns = [
    #path('reports', ReportView.as_view(), name='reports'),
     path('', views.ReportView.as_view(), name='reports'),

]
