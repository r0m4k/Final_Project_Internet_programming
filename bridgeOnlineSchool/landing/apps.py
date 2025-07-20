"""
Django App Configuration for Landing Module

This module configures the landing page application for the Bridge Online School
platform. Handles app-specific settings and initialization for the main public-facing
pages, teacher profiles, and review system functionality.
"""

from django.apps import AppConfig


class LandingConfig(AppConfig):
    """
    Configuration class for the landing Django application.
    
    Defines app-specific settings including default field types and
    application name for the main website functionality including
    teacher listings, profiles, and review system in the Bridge Online School platform.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing'
