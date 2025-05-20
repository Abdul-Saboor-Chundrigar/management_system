from django import forms
from .models import Region, DeviceType, DeviceComponent

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DeviceTypeForm(forms.ModelForm):
    class Meta:
        model = DeviceType
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'has_components': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DeviceComponentForm(forms.ModelForm):
    class Meta:
        model = DeviceComponent
        fields = '__all__'
        widgets = {
            'device_type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
