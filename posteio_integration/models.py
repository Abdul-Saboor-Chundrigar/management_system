from django.db import models

class PosteIOConfig(models.Model):
    api_token = models.CharField(max_length=100, blank=True, help_text="Poste.io admin API token")
    domain = models.CharField(max_length=100, default='itsupportserver.internal')
    smtp_host = models.CharField(max_length=100, default='mail.itsupportserver.internal')
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_username = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    imap_host = models.CharField(max_length=100, default='mail.itsupportserver.internal')
    imap_port = models.PositiveIntegerField(default=993)
    imap_username = models.CharField(max_length=100, blank=True)
    imap_password = models.CharField(max_length=100, blank=True)
    default_from_email = models.EmailField(default='no-reply@itsupportserver.internal')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Poste.io Config: {self.domain}"
