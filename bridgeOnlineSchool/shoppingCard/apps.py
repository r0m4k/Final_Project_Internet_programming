"""
Django App Configuration for Shopping Cart Module

This module configures the e-commerce application for the Bridge Online School
platform. Handles app-specific settings and initialization for shopping cart
functionality, checkout processing, and purchase management.
"""

from django.apps import AppConfig


class ShoppingcardConfig(AppConfig):
    """
    Configuration class for the shopping cart Django application.
    
    Defines app-specific settings including default field types and
    application name for the e-commerce functionality including
    cart management, checkout processing, and purchase tracking
    in the Bridge Online School platform.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shoppingCard'
