from django.db import models
from django.core.exceptions import ValidationError
from employee_management.models import Employee

def validate_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 MB
    if len(value) > max_size:
        raise ValidationError('File size cannot exceed 10 MB.')

class Attachment(models.Model):
    filename = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    file_data = models.BinaryField(validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, to_field='emp_number')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['filename', 'employee'], name='unique_attachment')
        ]

    def __str__(self):
        return f"{self.filename} (Employee: {self.employee.emp_number if self.employee else 'None'})"
