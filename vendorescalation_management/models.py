from django.db import models
from employee_management.models import Employee

class VendorEscalationManagement(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    DEVICE_TYPES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Printer', 'Printer'),
        ('Other', 'Other')
    ]

    date_created = models.DateField(auto_now_add=True)
    vendor_name = models.CharField(max_length=100)
    vendor_email = models.EmailField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)

    # Device details
    brand = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    serial_number = models.CharField(max_length=50, blank=True)
    aims_tag = models.CharField(max_length=50, blank=True)

    # Desktop-specific fields
    lcd_brand = models.CharField(max_length=50, blank=True, null=True)
    lcd_model = models.CharField(max_length=50, blank=True, null=True)
    lcd_serial = models.CharField(max_length=50, blank=True, null=True, unique=True)
    lcd_aims_tag = models.CharField(max_length=50, blank=True, null=True, unique=True)
    
    cpu_brand = models.CharField(max_length=50, blank=True, null=True)
    cpu_model = models.CharField(max_length=50, blank=True, null=True)
    cpu_serial = models.CharField(max_length=50, blank=True, null=True, unique=True)
    cpu_aims_tag = models.CharField(max_length=50, blank=True, null=True, unique=True)

    issue_details = models.TextField()
    poc_name = models.CharField(max_length=100)
    it_email = models.EmailField()
    poc_cell = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    closure_date = models.DateField(null=True, blank=True)
    closure_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.device_type} - {self.serial_number}"
