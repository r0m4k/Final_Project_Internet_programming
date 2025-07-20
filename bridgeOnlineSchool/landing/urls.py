"""
Landing Page URL Configuration

This module defines URL patterns for the main public-facing pages and
teacher management functionality in the Bridge Online School platform.
Includes routes for home page, teacher profiles, reviews, and admin operations.
"""

from django.urls import path
from . import views

app_name = 'landing' 

urlpatterns = [
    # Public pages and main navigation
    path("", views.home, name="home"),
    path("about-us/", views.about_us, name="about_us"),
    path("contact/", views.contact, name="contact"),
    
    # Teacher profile and review system
    path("teachers/<int:pk>", views.teacher, name="teacher"),
    path("teachers/<int:teacher_id>/review/", views.add_review, name="add_review"),
    
    # Administrative teacher management (staff only)
    path("admin/delete-review/<int:review_id>/", views.delete_review, name="delete_review"),
    path("admin/approve-teacher/<int:pk>/", views.approve_teacher, name="approve_teacher"),
    path("admin/delete-teacher/<int:pk>/", views.delete_teacher, name="delete_teacher"),
    path("admin/deactivate-teacher/<int:pk>/", views.deactivate_teacher, name="deactivate_teacher"),
]