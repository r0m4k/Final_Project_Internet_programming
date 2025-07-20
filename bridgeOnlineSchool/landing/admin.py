"""
Django Admin Configuration for Landing App

This module configures the Django admin interface for teacher and rating
management in the Bridge Online School platform. Registers models for
administrative access and content management.
"""

from django.contrib import admin
from . import models

# Register Teacher model for administrative management
admin.site.register(models.Teacher)

# Register Rating model for review management and moderation
admin.site.register(models.Rating)