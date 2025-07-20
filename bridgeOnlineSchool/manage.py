#!/usr/bin/env python
"""
Django Management Utility for Bridge Online School Platform

This is Django's command-line utility for administrative tasks in the
Bridge Online School project. Provides access to all Django management
commands including database migrations, static file collection, and
development server operations.

Usage:
    python manage.py <command> [options]

Common commands:
    - runserver: Start the development server
    - migrate: Apply database migrations
    - makemigrations: Create new database migrations
    - collectstatic: Collect static files for production
    - createsuperuser: Create administrative user account
"""
import os
import sys


def main():
    """
    Executes Django administrative tasks from the command line.
    
    Sets up the Django environment and delegates command execution
    to Django's built-in management system. Handles import errors
    and provides helpful error messages for common setup issues.
    
    Raises:
        ImportError: If Django is not properly installed or accessible
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridgeOnlineSchool.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()