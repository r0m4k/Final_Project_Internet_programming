"""
Django App Configuration for Authentication Module

This module configures the authentication application for the Bridge Online School
platform. Handles app-specific settings and initialization for user authentication,
registration, and profile management functionality.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration class for the authentication Django application.
    
    Defines app-specific settings including default field types and
    application name for the user authentication and profile management
    functionality in the Bridge Online School platform.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
