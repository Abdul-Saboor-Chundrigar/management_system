from django import forms

class ReportForm(forms.Form):
    REPORT_TYPES = (
        ('asset', 'Asset Report'),
        ('warehouse', 'Warehouse Report'),
        ('vendor', 'Vendor Report'),
    )
    
    EXPORT_FORMATS = (
        ('html', 'HTML'),
        ('csv', 'CSV'),
        ('pdf', 'PDF'),
        ('xlsx', 'Excel'),
        ('docx', 'Word'),
    )
    
    report_type = forms.ChoiceField(
        choices=REPORT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    export_format = forms.ChoiceField(
        choices=EXPORT_FORMATS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
