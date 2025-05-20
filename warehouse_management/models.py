from django.db import models
from employee_management.models import Employee
#from core.models import DeviceType, DeviceComponent

class Warehouse(models.Model):  # Renamed from Inventory
    DEVICE_TYPES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Printer', 'Printer'),
        ('Other', 'Other')
    ]
    REGIONS = [
        ('North', 'North'),
        ('South', 'South'),
        ('Central', 'Central')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) #, related_name='warehouse')
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    region = models.CharField(max_length=20, choices=REGIONS)
    #device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)
    
    # Common fields
    recepient_name = models.CharField(max_length=255)
    recepient_email = models.EmailField()
    recepient_cell = models.CharField(max_length=50)
    dispatcher = models.CharField(max_length=255)
    IT_email = models.EmailField()
    IT_cell = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, unique=True)
    aims_tag = models.CharField(max_length=50, unique=True)
   
    # Desktop-specific fields
    lcd_brand = models.CharField(max_length=50, blank=True, null=True)
    lcd_model = models.CharField(max_length=50, blank=True, null=True)
    lcd_serial = models.CharField(max_length=50, blank=True, null=True, unique=True)
    lcd_aims_tag = models.CharField(max_length=50, blank=True, null=True, unique=True)
    
    cpu_brand = models.CharField(max_length=50, blank=True, null=True)
    cpu_model = models.CharField(max_length=50, blank=True, null=True)
    cpu_serial = models.CharField(max_length=50, blank=True, null=True, unique=True)
    cpu_aims_tag = models.CharField(max_length=50, blank=True, null=True, unique=True)
    
    def __str__(self):
        return f"{self.device_type} - {self.serial_number}"


