from django.contrib import admin
from .models import Purchase, Checkout

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_id', 'user_profile', 'teacher_profile', 'number_of_lessons', 'total_price', 'status', 'date']
    list_filter = ['status', 'date', 'teacher_profile']
    search_fields = ['user_profile__username', 'teacher_profile__first_name', 'teacher_profile__last_name', 'purchase_id']
    readonly_fields = ['purchase_id', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date']
    
    fieldsets = (
        ('Purchase Information', {
            'fields': ('purchase_id', 'user_profile', 'teacher_profile', 'number_of_lessons', 'total_price', 'status')
        }),
        ('Details', {
            'fields': ('notes', 'communication_method')
        }),
        ('Timestamps', {
            'fields': ('date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['checkout_id', 'user', 'total_amount', 'payment_status', 'checkout_date', 'total_lessons_count']
    list_filter = ['payment_status', 'checkout_date', 'payment_method']
    search_fields = ['user__username', 'checkout_id', 'billing_email', 'billing_name']
    readonly_fields = ['checkout_id', 'created_at', 'updated_at', 'total_lessons_count', 'unique_teachers_count']
    date_hierarchy = 'checkout_date'
    ordering = ['-checkout_date']
    
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
        ('Statistics', {
            'fields': ('total_lessons_count', 'unique_teachers_count'),
            'classes': ('collapse',)
        }),
        ('Products', {
            'fields': ('products',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['products']
    
    def total_lessons_count(self, obj):
        return obj.total_lessons
    total_lessons_count.short_description = 'Total Lessons'
    
    def unique_teachers_count(self, obj):
        return obj.unique_teachers
    unique_teachers_count.short_description = 'Unique Teachers'
