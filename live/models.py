from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    ip = models.GenericIPAddressField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    nearby_landmark = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def clean(self):
        if self.latitude == 0 and self.longitude == 0:
            raise ValidationError("Coordinates cannot be (0,0)")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username} @ {self.city}"

