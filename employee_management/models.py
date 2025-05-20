from django.db import models
from core.models import Region

class Employee(models.Model):

    REGION_CHOICES = [
        ('North', 'North'),
        ('South', 'South'), 
        ('Central', 'Central'),
    ]
    
    CITY_CHOICES = [
        ('Karachi', 'Karachi'),
        ('Hyderabad', 'Hyderabad'),
        ('Sukkur', 'Sukkur'),
        ('NawabShah', 'NawabShah'),
        ('Larkana', 'Larkana'),
        ('Islamabad', 'Islamabad'),
        ('Lahore', 'Lahore'),
        ('Multan', 'Multan'),
        ('Sialkot', 'Sialkot'),
        ('Rawalpindi', 'Rawalpindi'),
    ]
    
    emp_number = models.CharField(max_length=20, unique=True)
    date_added = models.DateField(auto_now_add=True)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)  # Changed from ForeignKey
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    cell_phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)  # Added choices
    location = models.CharField(max_length=100)
    date_joined = models.DateField()
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.emp_number} - {self.name}"
