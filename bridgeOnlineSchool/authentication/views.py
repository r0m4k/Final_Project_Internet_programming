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
from landing.models import Teacher, Rating
from shoppingCard.models import Purchase
from django.utils import timezone
from datetime import timedelta
import random
import string
import re


def login_user(request):
    """
    Handles user authentication and login functionality.
    
    Validates user credentials and redirects to profile page upon successful authentication.
    Displays error message for invalid credentials.
    
    Args:
        request: HTTP request object containing login credentials
        
    Returns:
        HttpResponse: Redirect to profile page on success or login page with error
    """
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
    """
    Handles user logout and session termination.
    
    Clears user session and redirects to login page.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered login page template
    """
    logout(request)
    return render(request, "authentication/auth.html", {})


def register_user(request):
    """
    Handles new user registration with form validation.
    
    Creates new user account, authenticates the user, and redirects to profile page.
    Validates form data and displays errors if validation fails.
    
    Args:
        request: HTTP request object containing registration data
        
    Returns:
        HttpResponse: Redirect to profile on success or registration page with form
    """
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
    """
    Handles password reset requests by generating temporary passwords.
    
    Validates user email, generates a secure temporary password, and sends it via email.
    Users are required to change the temporary password upon next login.
    
    Args:
        request: HTTP request object containing email for password reset
        
    Returns:
        HttpResponse: Redirect to login page on success or password reset form
    """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generate a secure temporary password with mixed characters
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Update user password with the temporary password
            user.set_password(temp_password)
            user.save()
            
            # Send notification email with temporary password
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
    """
    Manages user profile page with account settings and teacher profile functionality.
    
    Handles both regular user account updates and teacher profile creation/updates.
    Supports password changes with complexity validation and teacher profile management.
    
    Args:
        request: HTTP request object containing profile update data
        
    Returns:
        HttpResponse: Rendered profile page or redirect to login if unauthenticated
    """
    if not request.user.is_authenticated:
        return redirect('authentication:login')

    # Retrieve existing teacher profile or set to None if not found
    try:
        teacher_profile = request.user.teacher_profile
    except Teacher.DoesNotExist:
        teacher_profile = None

    if request.method == 'POST':
        user = request.user
        changes_made = False

        # Determine which form was submitted based on form fields
        is_teacher_form = 'teacher_profile_submit' in request.POST
        
        # Fallback detection using teacher-specific field presence
        if not is_teacher_form:
            teacher_fields = ['title', 'experience', 'lesson_price', 'course_price']
            is_teacher_form = any(field in request.POST for field in teacher_fields)
        
        if is_teacher_form:
            # Process teacher profile form submission
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
                teacher.is_active = False  # Set as pending for admin approval
                teacher.save()
                return redirect('authentication:profile')
            else:
                # Display validation errors to user for correction
                for field, errors in teacher_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
                return redirect('authentication:profile')
        else:
            # Process account settings form submission
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

                # Define password complexity requirements for security validation
                password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')

                if new_password != confirm_password:
                    messages.error(request, 'The two password fields did not match.')
                elif not password_pattern.match(new_password):
                    messages.error(request, 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character.')
                else:
                    user.set_password(new_password)
                    update_session_auth_hash(request, user)  # Maintain user session after password change
                    changes_made = True

            if changes_made:
                user.save()
                # Synchronize teacher profile names with user account changes
                if teacher_profile:
                    teacher_profile.first_name = user.first_name
                    teacher_profile.last_name = user.last_name
                    teacher_profile.save()

            return redirect('authentication:profile')

    # Initialize teacher form for template rendering
    if teacher_profile:
        teacher_form = TeacherProfileForm(instance=teacher_profile)
    else:
        teacher_form = TeacherProfileForm()

    # Retrieve recent user activity for notifications dashboard
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Fetch recent lesson purchases for activity display
    recent_purchases = Purchase.objects.filter(
        user_profile=request.user,
        created_at__gte=thirty_days_ago
    ).select_related('teacher_profile').order_by('-created_at')[:5]
    
    # Fetch recent teacher reviews submitted by user
    recent_reviews = Rating.objects.filter(
        user=request.user,
        created_at__gte=thirty_days_ago
    ).select_related('teacher').order_by('-created_at')[:5]

    return render(request, 'authentication/profile.html', {
        'user': request.user,
        'teacher_profile': teacher_profile,
        'teacher_form': teacher_form,
        'recent_purchases': recent_purchases,
        'recent_reviews': recent_reviews,
    })
