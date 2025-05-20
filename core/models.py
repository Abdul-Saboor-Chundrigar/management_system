from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class DeviceType(models.Model):
    name = models.CharField(max_length=50)
    has_components = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class DeviceComponent(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.device_type.name} - {self.name}"
