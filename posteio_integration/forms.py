from django import forms
from .models import PosteIOConfig

class PosteIOConfigForm(forms.ModelForm):
    class Meta:
        model = PosteIOConfig
        fields = [
            'api_token', 'domain', 'smtp_host', 'smtp_port', 'smtp_username',
            'smtp_password', 'smtp_use_tls', 'imap_host', 'imap_port',
            'imap_username', 'imap_password', 'default_from_email'
        ]
        widgets = {
            'api_token': forms.PasswordInput(),
            'smtp_password': forms.PasswordInput(),
            'imap_password': forms.PasswordInput(),
        }
