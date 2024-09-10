# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('accounts/profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('403/', views.forbidden, name='forbidden'),  # Add this line
]