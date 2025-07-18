from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, ForgotPasswordForm, TeacherProfileForm
from django.core.mail import send_mail
from django.conf import settings
from landing.models import Teacher
import random
import string
import re


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
    """Profile page view with settings, messages, and teacher profile sections"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')

    # Get or create teacher profile if it doesn't exist
    try:
        teacher_profile = request.user.teacher_profile
    except Teacher.DoesNotExist:
        teacher_profile = None

    if request.method == 'POST':
        user = request.user
        changes_made = False

        # Debug: Print POST data to see what's being sent
        print("POST data keys:", list(request.POST.keys()))
        print("POST data:", dict(request.POST))

        # Check which form was submitted
        # Method 1: Check for teacher_profile_submit button
        is_teacher_form = 'teacher_profile_submit' in request.POST
        
        # Method 2: Check for teacher-specific fields as fallback
        if not is_teacher_form:
            teacher_fields = ['title', 'experience', 'lesson_price', 'course_price']
            is_teacher_form = any(field in request.POST for field in teacher_fields)
        
        if is_teacher_form:
            # Handle teacher profile form
            if teacher_profile:
                teacher_form = TeacherProfileForm(request.POST, request.FILES, instance=teacher_profile)
            else:
                teacher_form = TeacherProfileForm(request.POST, request.FILES)
            
            if teacher_form.is_valid():
                print("Teacher profile form is valid")
                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.first_name = user.first_name
                teacher.last_name = user.last_name
                teacher.is_active = False  # Set to True by default as requested
                teacher.save()
                return redirect('authentication:profile')
            else:
                print("Teacher profile form is invalid:", teacher_form.errors)
                # Add form errors to messages
                for field, errors in teacher_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
                return redirect('authentication:profile')
        else:
            # Handle account settings form
            # --- Account Info Update ---
            print("Handling account settings form")
            if user.first_name != request.POST.get('first_name'):
                user.first_name = request.POST.get('first_name')
                changes_made = True
            
            if user.last_name != request.POST.get('last_name'):
                user.last_name = request.POST.get('last_name')
                changes_made = True

            new_email = request.POST.get('email')
            if new_email and new_email != user.email:
                if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                    messages.error(request, 'This email is already in use.')
                else:
                    user.email = new_email
                    changes_made = True

            new_username = request.POST.get('username')
            if new_username and new_username != user.username:
                if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                    messages.error(request, 'This username is already taken.')
                else:
                    user.username = new_username
                    changes_made = True

            # --- Password Change ---
            new_password = request.POST.get('new_password')
            if new_password:
                confirm_password = request.POST.get('confirm_password')

                # Password complexity regex: min 8 chars, 1 letter, 1 number, 1 special char
                password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

                if new_password != confirm_password:
                    messages.error(request, 'The two password fields did not match.')
                elif not password_pattern.match(new_password):
                    messages.error(request, 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character.')
                else:
                    user.set_password(new_password)
                    update_session_auth_hash(request, user)  # Important!
                    changes_made = True

            if changes_made:
                user.save()
                # Update teacher profile names if they exist
                if teacher_profile:
                    teacher_profile.first_name = user.first_name
                    teacher_profile.last_name = user.last_name
                    teacher_profile.save()

            return redirect('authentication:profile')

    # Create teacher form for rendering
    if teacher_profile:
        teacher_form = TeacherProfileForm(instance=teacher_profile)
    else:
        teacher_form = TeacherProfileForm()

    return render(request, 'authentication/profile.html', {
        'user': request.user,
        'teacher_profile': teacher_profile,
        'teacher_form': teacher_form
    })
