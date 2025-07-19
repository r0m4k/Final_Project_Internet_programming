from django.db import models
from django.contrib.auth.models import User
from landing.models import Teacher
from django.utils import timezone
import uuid

class Purchase(models.Model):
    """Model to represent individual lesson purchases"""
    purchase_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    teacher_profile = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lesson_purchases')
    number_of_lessons = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Additional fields for better functionality
    notes = models.TextField(blank=True, help_text='Special notes for the teacher')
    communication_method = models.CharField(max_length=100, blank=True, help_text='Preferred communication method')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
    
    def __str__(self):
        return f"Purchase {self.purchase_id} - {self.user_profile.username} -> {self.teacher_profile.first_name} {self.teacher_profile.last_name}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total_price if not set
        if not self.total_price:
            self.total_price = self.teacher_profile.lesson_price * self.number_of_lessons
        super().save(*args, **kwargs)


class Checkout(models.Model):
    """Model to represent a complete checkout session containing multiple purchases"""
    checkout_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    products = models.ManyToManyField(Purchase, related_name='checkouts', blank=True)
    
    # Additional checkout information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    checkout_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Payment and status information
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    payment_method = models.CharField(max_length=50, blank=True, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
    ])
    
    transaction_id = models.CharField(max_length=255, blank=True, help_text='External payment processor transaction ID')
    
    # Contact information
    billing_email = models.EmailField()
    billing_name = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-checkout_date']
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'
    
    def __str__(self):
        return f"Checkout {self.checkout_id} - {self.user.username} (${self.total_amount})"
    
    def calculate_total(self):
        """Calculate total amount from all associated purchases"""
        total = sum(purchase.total_price for purchase in self.products.all())
        return total
    
    def save(self, *args, **kwargs):
        # Auto-calculate total_amount if not set
        if self.pk:  # Only if the checkout already exists (has products)
            self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)
    
    @property
    def total_lessons(self):
        """Get total number of lessons in this checkout"""
        return sum(purchase.number_of_lessons for purchase in self.products.all())
    
    @property
    def unique_teachers(self):
        """Get count of unique teachers in this checkout"""
        return self.products.values('teacher_profile').distinct().count()
