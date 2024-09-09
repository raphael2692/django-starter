from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import UserEditForm

def home(request):
    return render(request, 'home.html')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})
