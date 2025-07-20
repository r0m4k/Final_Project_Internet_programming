"""
Main URL Configuration for Bridge Online School Platform

This module defines the root URL patterns for the Bridge Online School
Django project. Includes routing to all major application modules and
media file serving configuration for development.
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    # Main website and landing pages
    path("", include("landing.urls")),
    
    # User authentication and profile management
    path("authentication/", include("authentication.urls")),
    
    # Shopping cart and e-commerce functionality
    path("cart/", include("shoppingCard.urls")),
    
    # Django admin interface
    path("admin/", admin.site.urls),
    
    # Media file serving configuration for development environment
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
