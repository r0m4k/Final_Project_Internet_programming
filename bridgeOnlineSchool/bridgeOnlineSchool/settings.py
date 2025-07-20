"""
Django Configuration for Bridge Online School Platform

This module contains all configuration settings for the Bridge Online School
web application, including database connections, static file handling,
installed applications, and security configurations.

Built on Django 5.2.3

For deployment considerations, see:
https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
"""

from pathlib import Path

# Project root directory path configuration
BASE_DIR = Path(__file__).resolve().parent.parent


# Security Configuration
# For production deployment, these settings must be updated for security

# Django secret key - MUST be changed for production deployment
SECRET_KEY = 'django-insecure-6e$z!2c@h^og!*y3m-$3bsjv%0&zjh0clrp^4)w#2&d)7k51i*'

# Debug mode - MUST be disabled for production deployment
DEBUG = False

# Allowed host domains - MUST be configured for production deployment
ALLOWED_HOSTS = ['*']


# Django Application Registry

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'landing',
    'authentication',
    'shoppingCard',  # Shopping cart and checkout functionality
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add this for WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'bridgeOnlineSchool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bridgeOnlineSchool.wsgi.application'


# Database Configuration
# Currently using SQLite for development - consider PostgreSQL for production

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# User Authentication Password Validation
# Enforces strong password requirements for user security

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Add this for project-level static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# For production - where collected static files will be stored
STATIC_ROOT = BASE_DIR / 'staticfiles'

# URLS FOR IMAGES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'online.bridge.school@gmail.com'  # Your email
EMAIL_HOST_PASSWORD = 'hebn sdhd oihw eiqk'  # Your app password (not regular password)
DEFAULT_FROM_EMAIL = 'online.bridge.school@gmail.com'
