from django.contrib import admin
from .models import Attachment

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'description', 'employee_number', 'created_at')
    search_fields = ('filename', 'description', 'employee__emp_number', 'employee__name')

    def employee_number(self, obj):
        return obj.employee.emp_number if obj.employee else 'None'
    employee_number.short_description = 'Employee Number'
