"""
Django Admin Configuration for Shopping Cart and E-commerce

This module configures the Django admin interface for managing purchases
and checkout transactions in the Bridge Online School platform. Provides
comprehensive administrative tools for order management, customer support,
and financial tracking.
"""

from django.contrib import admin
from .models import Purchase, Checkout


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """
    Administrative interface for individual lesson purchase management.
    
    Provides comprehensive tools for viewing, filtering, and managing
    individual lesson purchases. Includes search functionality, status
    tracking, and detailed purchase information organization.
    """
    
    # Display configuration for purchase list view
    list_display = ['purchase_id', 'user_profile', 'teacher_profile', 'number_of_lessons', 'total_price', 'status', 'date']
    list_filter = ['status', 'date', 'teacher_profile']
    search_fields = ['user_profile__username', 'teacher_profile__first_name', 'teacher_profile__last_name', 'purchase_id']
    readonly_fields = ['purchase_id', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date']
    
    # Organized field layout for purchase detail view
    fieldsets = (
        ('Purchase Information', {
            'fields': ('purchase_id', 'user_profile', 'teacher_profile', 'number_of_lessons', 'total_price', 'status')
        }),
        ('Communication Details', {
            'fields': ('notes', 'communication_method')
        }),
        ('Timestamps', {
            'fields': ('date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    """
    Administrative interface for checkout transaction management.
    
    Provides comprehensive tools for managing complete checkout sessions,
    payment tracking, and order analysis. Includes custom methods for
    calculating transaction statistics and managing related purchases.
    """
    
    # Display configuration for checkout list view
    list_display = ['checkout_id', 'user', 'total_amount', 'payment_status', 'checkout_date', 'total_lessons_count']
    list_filter = ['payment_status', 'checkout_date', 'payment_method']
    search_fields = ['user__username', 'checkout_id', 'billing_email', 'billing_name']
    readonly_fields = ['checkout_id', 'created_at', 'updated_at', 'total_lessons_count', 'unique_teachers_count']
    date_hierarchy = 'checkout_date'
    ordering = ['-checkout_date']
    
    # Organized field layout for checkout detail view
    fieldsets = (
        ('Checkout Information', {
            'fields': ('checkout_id', 'user', 'checkout_date', 'total_amount', 'payment_status')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'transaction_id')
        }),
        ('Billing Information', {
            'fields': ('billing_email', 'billing_name')
        }),
        ('Transaction Statistics', {
            'fields': ('total_lessons_count', 'unique_teachers_count'),
            'classes': ('collapse',)
        }),
        ('Associated Purchases', {
            'fields': ('products',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Enhanced interface for managing related purchases
    filter_horizontal = ['products']
    
    def total_lessons_count(self, obj):
        """
        Calculates the total number of lessons across all purchases in checkout.
        
        Args:
            obj: Checkout instance
            
        Returns:
            int: Total lesson count for display in admin list
        """
        return obj.total_lessons
    total_lessons_count.short_description = 'Total Lessons'
    
    def unique_teachers_count(self, obj):
        """
        Calculates the number of unique teachers in the checkout.
        
        Args:
            obj: Checkout instance
            
        Returns:
            int: Unique teacher count for display in admin list
        """
        return obj.unique_teachers
    unique_teachers_count.short_description = 'Unique Teachers'
