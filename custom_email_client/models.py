from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

class EmailStorageQuota(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_quota')
    storage_used = models.FloatField(default=0)  # MB
    storage_limit = models.FloatField(default=2)  # Initial 2 MB

    def can_store(self, email_size_mb):
        stat = os.statvfs('/')
        free_space_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
        if free_space_mb > 100 and self.storage_limit < 10:
            self.storage_limit = min(self.storage_limit + email_size_mb, 10)
            self.save()
        if self.storage_used + email_size_mb <= self.storage_limit:
            self.storage_used += email_size_mb
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}: {self.storage_used}/{self.storage_limit} MB"

class EmailMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.EmailField()
    recipient = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True, null=True)
    received_at = models.DateTimeField(null=True, blank=True)
    size_mb = models.FloatField()
    app_name = models.CharField(max_length=50, blank=True)
    is_sent = models.BooleanField(default=False)
    vendor = models.ForeignKey('vendorescalation_management.VendorEscalationManagement', on_delete=models.SET_NULL, null=True, blank=True)
    is_test = models.BooleanField(default=False)

    def clean(self):
        quota = EmailStorageQuota.objects.get_or_create(user=self.user)[0]
        if not quota.can_store(self.size_mb):
            raise ValidationError("Storage limit exceeded for this user.")

    def __str__(self):
        return f"{self.subject} - {self.user.username}"

class EmailAttachment(models.Model):
    email = models.ForeignKey(EmailMessage, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='email_attachments/')
    size_mb = models.FloatField()

    def save(self, *args, **kwargs):
        self.size_mb = self.file.size / (1024 * 1024)
        super().save(*args, **kwargs)
