from django.db import models
#from authentication.models import CustomUser

class Attendance(models.Model):
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    auth_method = models.CharField(max_length=20, choices=[
        ('PASSWORD', 'Password'),
        ('BIOMETRIC', 'Biometric')
    ])

    @property
    def duration(self):
        if self.check_out:
            return self.check_out - self.check_in
        return None

    def __str__(self):
        return f"{self.user.username} - {self.check_in}"
