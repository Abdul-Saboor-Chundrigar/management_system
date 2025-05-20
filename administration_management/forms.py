from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    create_posteio_email = forms.BooleanField(required=False, label="Create Poste.io email account")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'create_posteio_email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                create_posteio_email=self.cleaned_data['create_posteio_email']
            )
        return user
