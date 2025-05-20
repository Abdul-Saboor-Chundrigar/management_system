from django.db import models

class ScanRecord(models.Model):
    netbios_name = models.CharField(max_length=255, blank=True)
    ipv4_address = models.CharField(max_length=15, blank=True)
    scan_time = models.DateTimeField(auto_now_add=True)
    hardware_details = models.JSONField()
    software_details = models.JSONField()

    def __str__(self):
        return f"{self.netbios_name or self.ipv4_address} - {self.scan_time}"

    class Meta:
        ordering = ['-scan_time']
