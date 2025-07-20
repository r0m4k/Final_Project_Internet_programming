"""
Shopping Cart and E-commerce Views Module

This module handles all shopping cart functionality, checkout processing,
and purchase management for the Bridge Online School platform. Implements
a client-side cart system using localStorage with server-side checkout processing.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from decimal import Decimal

from landing.models import Teacher
from .models import Purchase, Checkout


def add_to_cart(request, teacher_id):
    """
    Retrieves teacher data for client-side cart management.
    
    Provides teacher information in JSON format for localStorage-based
    shopping cart functionality. Supports both AJAX and standard requests.
    
    Args:
        request: HTTP request object
        teacher_id: Primary key of the teacher to add to cart
        
    Returns:
        JsonResponse: Teacher data for AJAX requests
        HttpResponse: Rendered cart page for standard requests
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    # Prepare teacher data for client-side cart storage
    teacher_data = {
        'id': teacher.id,
        'first_name': teacher.first_name,
        'last_name': teacher.last_name,
        'title': teacher.title,
        'lesson_price': float(teacher.lesson_price),
        'avatar_url': teacher.avatar.url,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'teacher': teacher_data})
    
    # Fallback for non-AJAX requests
    return render(request, 'shoppingCard/cart.html', {'teacher_data': json.dumps(teacher_data)})


def view_cart(request):
    """
    Displays the shopping cart management page.
    
    Renders the cart interface where users can review, modify, and
    proceed to checkout with their selected lesson packages.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered shopping cart page template
    """
    return render(request, 'shoppingCard/cart.html')


def get_cart_count(request):
    """
    Legacy API endpoint for cart item counting.
    
    Maintained for compatibility with older implementations.
    Current cart system uses client-side localStorage management.
    
    Args:
        request: HTTP request object
        
    Returns:
        JsonResponse: Cart count (always returns 0 for localStorage system)
    """
    # This endpoint is no longer needed with localStorage, but keeping for compatibility
    return JsonResponse({'count': 0})


@login_required
def checkout_form(request):
    """
    Displays the checkout form for payment processing.
    
    Renders the checkout interface where authenticated users can
    review their cart and complete the payment process.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered checkout form template
    """
    return render(request, 'shoppingCard/checkout_form.html')


@login_required
@require_POST
def create_checkout(request):
    """
    Processes checkout data and creates purchase records.
    
    Converts client-side cart data into server-side Purchase and Checkout
    models. Handles transaction processing, error management, and data validation.
    Implements atomic operations to ensure data consistency.
    
    Args:
        request: HTTP request object containing JSON cart data
        
    Returns:
        JsonResponse: Success status with checkout ID or error details
    """
    try:
        # Parse and validate incoming cart data
        data = json.loads(request.body)
        
        # Validate required checkout fields
        if not data.get('items') or not data.get('total_amount'):
            return JsonResponse({
                'success': False,
                'message': 'Invalid cart data'
            })
        
        # Create primary checkout record
        checkout = Checkout.objects.create(
            user=request.user,
            total_amount=Decimal(str(data['total_amount'])),
            billing_email=data.get('billing_email', request.user.email),
            billing_name=data.get('billing_name', request.user.get_full_name() or request.user.username),
            payment_method=data.get('payment_method', 'credit_card'),
            transaction_id=data.get('transaction_id', ''),
            payment_status='completed'  # Set to completed for demo purposes
        )
        
        # Process individual lesson purchases
        purchases = []
        for item in data['items']:
            try:
                teacher = Teacher.objects.get(id=item['teacher_id'])
                
                purchase = Purchase.objects.create(
                    user_profile=request.user,
                    teacher_profile=teacher,
                    number_of_lessons=item['number_of_lessons'],
                    total_price=Decimal(str(item['total_price'])),
                    notes=item.get('notes', ''),
                    communication_method=item.get('communication_method', ''),
                    status='pending'
                )
                purchases.append(purchase)
                
            except Teacher.DoesNotExist:
                # Implement atomic rollback on errors
                checkout.delete()
                for p in purchases:
                    p.delete()
                return JsonResponse({
                    'success': False,
                    'message': f'Teacher with ID {item["teacher_id"]} not found'
                })
            except Exception as e:
                # Implement atomic rollback on errors
                checkout.delete()
                for p in purchases:
                    p.delete()
                return JsonResponse({
                    'success': False,
                    'message': f'Error creating purchase: {str(e)}'
                })
        
        # Associate all purchases with checkout record
        checkout.products.set(purchases)
        checkout.save()  # Triggers total amount recalculation
        
        return JsonResponse({
            'success': True,
            'checkout_id': str(checkout.checkout_id),
            'message': 'Checkout created successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating checkout: {str(e)}'
        })


@login_required
def checkout_success(request):
    """
    Displays successful checkout confirmation page.
    
    Shows order details and purchase confirmation for completed transactions.
    Validates checkout ownership and provides purchase summary.
    
    Args:
        request: HTTP request object with checkout_id parameter
        
    Returns:
        HttpResponse: Rendered success page or redirect to cart on error
    """
    checkout_id = request.GET.get('checkout_id')
    
    if not checkout_id:
        messages.error(request, 'No checkout ID provided')
        return redirect('shoppingCard:cart')
    
    try:
        checkout = Checkout.objects.get(checkout_id=checkout_id, user=request.user)
        
        context = {
            'checkout': checkout,
            'purchases': checkout.products.all(),
        }
        return render(request, 'shoppingCard/checkout_success.html', context)
        
    except Checkout.DoesNotExist:
        messages.error(request, 'Checkout not found')
        return redirect('shoppingCard:cart')


@login_required
def my_purchases(request):
    """
    Displays user's complete purchase and checkout history.
    
    Provides comprehensive view of all lesson purchases and transactions
    for the authenticated user, ordered by most recent first.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered purchase history page template
    """
    purchases = Purchase.objects.filter(user_profile=request.user).order_by('-date')
    checkouts = Checkout.objects.filter(user=request.user).order_by('-checkout_date')
    
    context = {
        'purchases': purchases,
        'checkouts': checkouts,
    }
    return render(request, 'shoppingCard/my_purchases.html', context)


@login_required
def purchase_detail(request, purchase_id):
    """
    Displays detailed information for a specific lesson purchase.
    
    Shows comprehensive purchase details including teacher information,
    lesson details, pricing, and communication preferences.
    
    Args:
        request: HTTP request object
        purchase_id: UUID of the specific purchase to display
        
    Returns:
        HttpResponse: Rendered purchase detail page template
    """
    purchase = get_object_or_404(Purchase, purchase_id=purchase_id, user_profile=request.user)
    
    context = {
        'purchase': purchase,
    }
    return render(request, 'shoppingCard/purchase_detail.html', context)


@login_required
def checkout_detail(request, checkout_id):
    """
    Displays comprehensive details for a specific checkout transaction.
    
    Shows complete checkout information including all associated purchases,
    payment details, and transaction status.
    
    Args:
        request: HTTP request object
        checkout_id: UUID of the specific checkout to display
        
    Returns:
        HttpResponse: Rendered checkout detail page template
    """
    checkout = get_object_or_404(Checkout, checkout_id=checkout_id, user=request.user)
    
    context = {
        'checkout': checkout,
        'purchases': checkout.products.all(),
    }
    return render(request, 'shoppingCard/checkout_detail.html', context)
