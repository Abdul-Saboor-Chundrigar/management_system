from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Add this
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    activity_type = models.CharField(max_length=50)  # 'login', 'logout', 'page_view'
    url = models.CharField(max_length=500, null=True, blank=True)
    details = models.JSONField(default=dict)  # Stores additional metadata

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
