from django import forms
from .models import VendorEscalationManagement
from employee_management.models import Employee
# from core.models import DeviceType, DeviceComponent
from django.core.validators import validate_email

class VendorEscalationManagementForm(forms.ModelForm):
    it_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[validate_email]
    )

    class Meta:
        model = VendorEscalationManagement
        fields = '__all__'
        widgets = {
            'device_type': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'toggleFields()'
            }),
            'date_assigned': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        closure_date = cleaned_data.get('closure_date')
        closure_remarks = cleaned_data.get('closure_remarks')

        if status == 'RESOLVED' and not closure_remarks:
            self.add_error('closure_remarks', 'Closure remarks are required when status is Resolved')

        return cleaned_data
