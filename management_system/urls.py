from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from two_factor_auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
    path('2fa/', include('two_factor_auth.urls')),
    path('employees/', include('employee_management.urls')),
    path('assets/', include('asset_management.urls')),
    path('warehouse/', include('warehouse_management.urls')),
    path('vendor-escalation/', include('vendorescalation_management.urls')),
    path('location_details/', include('live.urls')),
    path('search/', include('search.urls')),
    path('activity_dashboard/', include('user_activity.urls')),
    path('reports/', include('report_generation.urls')),

    path('email/', include('custom_email_client.urls')),
    path('posteio/', include('posteio_integration.urls')),



    path('administration/', include('administration_management.urls')),
  
    path('scan_hardware/', include('scan_hardware.urls')),

    path('file_attachment/', include('file_attachment.urls')),
    path('email_management/', include('email_management.urls')),

    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
]   

#  Add this at the end of the file
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
