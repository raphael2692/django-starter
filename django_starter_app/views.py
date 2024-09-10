from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .forms import AdminUserEditForm, UserEditForm, UserCreateForm
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_required(function):
    """Decorator to check if the user is an admin."""
    return user_passes_test(lambda u: u.is_superuser, login_url='forbidden')(function)

@login_required
def home(request):
    return render(request, 'home.html')

@admin_required
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if not request.user.is_superuser and request.user != user:
        # Regular users can only edit their own profile
        raise PermissionDenied
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect('user_profile')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'edit_profile.html', {'form': form})

@admin_required
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if not request.user.is_superuser and request.user != user:
        # Regular users can only edit their own profile
        raise PermissionDenied
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
   
    else:
        form = AdminUserEditForm(instance=user)
    
    return render(request, 'edit_user.html', {'form': form})

@admin_required
@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreateForm()
    
    return render(request, 'create_user.html', {'form': form})

@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)

def forbidden(request):
    return render(request, '403.html', status=403)
