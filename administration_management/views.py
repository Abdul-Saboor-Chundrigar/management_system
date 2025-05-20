from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm
from .models import AppPermission, UserProfile, APP_CHOICES, PERMISSION_LEVELS
from posteio_integration.views import create_posteio_account

def check_admin_permission(user, app_name):
    return AppPermission.objects.filter(user=user, app_name=app_name, permission_level='admin').exists()

@login_required
def dashboard(request):
    return render(request, 'administration_management/dashboard.html')

@login_required
def user_list(request):
    if not check_admin_permission(request.user, 'administration_management'):
        messages.error(request, "Admin access required")
        return redirect('administration_management:dashboard')
    users = User.objects.all()
    return render(request, 'administration_management/user_list.html', {'users': users})

@login_required
def manage_users(request):
    if not check_admin_permission(request.user, 'administration_management'):
        messages.error(request, "Admin access required")
        return redirect('administration_management:dashboard')
    users = User.objects.all()
    apps = [app[0] for app in APP_CHOICES]
    return render(request, 'administration_management/manage_users.html', {
        'users': users,
        'apps': apps,
        'permission_levels': PERMISSION_LEVELS,
    })

@login_required
def create_user(request):
    if not check_admin_permission(request.user, 'administration_management'):
        messages.error(request, "Admin access required")
        return redirect('administration_management:dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.get(user=user)
            if profile.create_posteio_email:
                email = user.email
                password = form.cleaned_data['password1']
                if create_posteio_account(user, email, password):
                    messages.success(request, f"User and Poste.io email account created: {email}")
                else:
                    messages.warning(request, "User created, but failed to create Poste.io email account.")
            else:
                messages.success(request, "User created without Poste.io email account.")
            return redirect('administration_management:manage_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'administration_management/create_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    if not check_admin_permission(request.user, 'administration_management'):
        messages.error(request, "Admin access required")
        return redirect('administration_management:dashboard')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        if username and email:
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exclude(id=user_id).exists():
                messages.error(request, "Email already exists")
            else:
                user.username = username
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                if password:
                    user.password = make_password(password)
                user.save()
                messages.success(request, f"User {username} updated successfully")
                return redirect('administration_management:manage_users')
        else:
            messages.error(request, "Username and email are required")
    return render(request, 'administration_management/edit_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    if not check_admin_permission(request.user, 'administration_management'):
        messages.error(request, "Admin access required")
        return redirect('administration_management:dashboard')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User {username} deleted successfully")
        return redirect('administration_management:manage_users')
    return render(request, 'administration_management/delete_user.html', {'user': user})

@login_required
def update_permissions(request, user_id):
    if not check_admin_permission(request.user, 'administration_management'):
        messages.error(request, "Admin access required")
        return redirect('administration_management:dashboard')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        AppPermission.objects.filter(user=user).delete()
        for app in APP_CHOICES:
            app_name = app[0]
            permission_level = request.POST.get(f'permission_{app_name}')
            if permission_level in [level[0] for level in PERMISSION_LEVELS]:
                AppPermission.objects.create(
                    user=user,
                    app_name=app_name,
                    permission_level=permission_level
                )
        messages.success(request, f"Permissions updated for {user.username}")
        return redirect('administration_management:manage_users')
    permissions = AppPermission.objects.filter(user=user)
    return render(request, 'administration_management/update_permissions.html', {
        'user': user,
        'apps': APP_CHOICES,
        'permission_levels': PERMISSION_LEVELS,
        'permissions': permissions,
    })
