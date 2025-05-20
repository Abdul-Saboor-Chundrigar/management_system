from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all fields as not required initially
        for field in self.fields:
            self.fields[field].required = False
        
        # Make common fields required
        common_fields = ['brand', 'model', 'serial_number', 'aims_tag']
        for field in common_fields:
            self.fields[field].required = True
