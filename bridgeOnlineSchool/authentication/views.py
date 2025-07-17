from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, ForgotPasswordForm
import random
import string


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('authentication:profile')
        else:
            error = "Invalid username or password."
            return render(request, "authentication/auth.html", {"error": error})

    return render(request, "authentication/auth.html", {})

def logout_user(request):
    logout(request)
    return render(request, "authentication/auth.html", {})


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('authentication:profile')
        else:
            return render(request, "authentication/register.html", {"form": form})


    return render(request, "authentication/register.html", {"form": form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generate a temporary password
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Set the new password
            user.set_password(temp_password)
            user.save()
            
            # Send email with temporary password
            subject = 'Your Temporary Password - Bridge Online School'
            message = f'''
Hello {user.username},
You requested a password reset for your Bridge Online School account.

Your temporary password is: {temp_password}

Please log in with this temporary password and change it immediately in your account settings.

Best regards,
Bridge Online School Team
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('authentication:login')
    else:
        form = ForgotPasswordForm()

    return render(request, 'authentication/forgot_password.html', {'form': form})


def profile_view(request):
    """Profile page view with settings and messages sections"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    return render(request, 'authentication/profile.html', {
        'user': request.user
    })
