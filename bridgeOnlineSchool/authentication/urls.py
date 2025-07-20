"""
Authentication URL Configuration

This module defines URL patterns for user authentication and account management
in the Bridge Online School platform. Includes routes for login, logout,
registration, password recovery, and user profile management.
"""

from django.urls import path
from . import views

app_name = 'authentication' 

urlpatterns = [
    # User authentication endpoints
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    
    # User registration and account creation
    path("register", views.register_user, name="register"),
    
    # Password recovery functionality
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    
    # User profile and account management
    path('profile/', views.profile_view, name='profile'),
]