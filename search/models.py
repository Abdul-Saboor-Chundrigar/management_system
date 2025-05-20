from django.db import models

class SearchLog(models.Model):
    query = models.CharField(max_length=100)
    field = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.field}: {self.query} by {self.user}"
