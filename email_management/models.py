from django.db import models

class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    app_name = models.CharField(max_length=50)
    record_id = models.CharField(max_length=50)  # e.g., emp_number, vendor_id

    def __str__(self):
        return f"Email to {self.recipient} from {self.app_name} at {self.sent_at}"

    class Meta:
        ordering = ['-sent_at']
