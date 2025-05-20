import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PosteIOConfig
from .forms import PosteIOConfigForm
from django.contrib.auth.models import User

@login_required
def configure_posteio(request):
    config = PosteIOConfig.objects.first()
    if request.method == 'POST':
        form = PosteIOConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Poste.io configuration updated.")
            return redirect('custom_email_client:email_list')
    else:
        form = PosteIOConfigForm(instance=config)
    return render(request, 'posteio_integration/configure_posteio.html', {'form': form})

def create_posteio_account(user, email, password):
    config = PosteIOConfig.objects.first()
    if not config or not config.api_token:
        return False
    url = f"https://{config.domain}/api/v1/mailboxes"
    headers = {'Authorization': f"Bearer {config.api_token}"}
    data = {
        'email': email,
        'password': password,
        'name': user.get_full_name() or user.username
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code == 201
    except Exception:
        return False
