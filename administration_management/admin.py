# administration_management/admin.py
from django.contrib import admin
from .models import AppPermission

@admin.register(AppPermission)
class AppPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'app_name', 'permission_level')
    list_filter = ('app_name', 'permission_level')
    search_fields = ('user__username', 'app_name')

