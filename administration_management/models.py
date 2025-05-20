# administration_management/models.py
from django.db import models
from django.contrib.auth.models import User, Group

# List of apps in the project
APP_CHOICES = [
    ('administration_management', 'Administration Management'),
    ('employee_management', 'Employee Management'),
    ('asset_management', 'Asset Management'),
    ('warehouse_management', 'Warehouse Management'),
    ('vendorescalation_management', 'Vendor Escalation Management'),
    ('report_generation', 'Report Generation'),
    ('search', 'Search'),
    ('user_activity', 'User Activity'),
    ('file_management', 'File Management'),
    ('custom_email_client', 'Cusyom Email Client'),
    ('scan_hardware', 'Scan Hardware'),
    ('live', 'Live'),
    ('two_factor_auth', 'Two Factor Auth'),
]

# Permission levels
PERMISSION_LEVELS = [
    ('read', 'Read'),
    ('write', 'Write'),
    ('admin', 'Admin'),
]

class AppPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_permissions')
    app_name = models.CharField(max_length=50)
    permission_level = models.CharField(max_length=20, choices=[
        ('read', 'Read'),
        ('write', 'Write'),
        ('admin', 'Admin')
    ])

    def __str__(self):
        return f"{self.user.username} - {self.app_name} - {self.permission_level}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_posteio_email = models.BooleanField(default=False, help_text="Create Poste.io email account")

    def __str__(self):
        return self.user.username

