from django import forms
from administration_management.models import APP_CHOICES
from vendorescalation_management.models import VendorEscalationManagement

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea(attrs={'id': 'email-body'}))
    recipient = forms.EmailField()
    app_name = forms.ChoiceField(choices=APP_CHOICES, required=False)
    vendor = forms.ModelChoiceField(queryset=VendorEscalationManagement.objects.all(), required=False)
    attachments = forms.FileField(widget=forms.FileInput(attrs={'allow_multiple_selected': True}), required=False)

class TestEmailForm(forms.Form):
    recipient = forms.EmailField()
    subject = forms.CharField(max_length=255, initial="Test Email")
    body = forms.CharField(widget=forms.Textarea, initial="This is a test email from Management System.")
