from django import forms
from .models import Warehouse
from employee_management.models import Employee
#from core.models import DeviceType, DeviceComponent

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
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




"""['employee', 'device_type', 'brand', 'model', 'serial_number', 'aims_tag', 
                  'recepient_name', 'recepient_email', 'recepient_cell', 'dispatcher', 
                  'IT_email', 'IT_cell', 'lcd_component', 'cpu_component']
        widgets = {
            'date_assigned': forms.DateInput(attrs={'readonly': 'readonly'}),
            
           
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'aims_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'lcd_component': forms.Select(attrs={'class': 'form-select'}),
            'cpu_component': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lcd_component'].queryset = DeviceComponent.objects.filter(
            device_type__name='Desktop', 
            name='LCD'
        )
        self.fields['cpu_component'].queryset = DeviceComponent.objects.filter(
            device_type__name='Desktop', 
            name='CPU'
        )
"""
