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
    """Get teacher data for adding to localStorage cart"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    # Return teacher data as JSON for localStorage
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
    
    # For non-AJAX requests, redirect to cart page
    return render(request, 'shoppingCard/cart.html', {'teacher_data': json.dumps(teacher_data)})

def view_cart(request):
    """Display the shopping cart page"""
    return render(request, 'shoppingCard/cart.html')

def get_cart_count(request):
    """Get total number of items in cart from localStorage (client-side handled)"""
    # This endpoint is no longer needed with localStorage, but keeping for compatibility
    return JsonResponse({'count': 0})

@login_required
def checkout_form(request):
    """Display the checkout form page"""
    return render(request, 'shoppingCard/checkout_form.html')

@login_required
@require_POST
def create_checkout(request):
    """Create a checkout and associated purchases from cart data"""
    try:
        # Parse JSON data from request
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('items') or not data.get('total_amount'):
            return JsonResponse({
                'success': False,
                'message': 'Invalid cart data'
            })
        
        # Create checkout object
        checkout = Checkout.objects.create(
            user=request.user,
            total_amount=Decimal(str(data['total_amount'])),
            billing_email=data.get('billing_email', request.user.email),
            billing_name=data.get('billing_name', request.user.get_full_name() or request.user.username),
            payment_method=data.get('payment_method', 'credit_card'),
            transaction_id=data.get('transaction_id', ''),
            payment_status='completed'  # Set to completed for demo purposes
        )
        
        # Create individual purchases
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
                # Clean up on error
                checkout.delete()
                for p in purchases:
                    p.delete()
                return JsonResponse({
                    'success': False,
                    'message': f'Teacher with ID {item["teacher_id"]} not found'
                })
            except Exception as e:
                # Clean up on error
                checkout.delete()
                for p in purchases:
                    p.delete()
                return JsonResponse({
                    'success': False,
                    'message': f'Error creating purchase: {str(e)}'
                })
        
        # Associate purchases with checkout
        checkout.products.set(purchases)
        checkout.save()  # This will recalculate total_amount
        
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
    """Display checkout success page"""
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
    """Display user's purchase history"""
    purchases = Purchase.objects.filter(user_profile=request.user).order_by('-date')
    checkouts = Checkout.objects.filter(user=request.user).order_by('-checkout_date')
    
    context = {
        'purchases': purchases,
        'checkouts': checkouts,
    }
    return render(request, 'shoppingCard/my_purchases.html', context)

@login_required
def purchase_detail(request, purchase_id):
    """Display details of a specific purchase"""
    purchase = get_object_or_404(Purchase, purchase_id=purchase_id, user_profile=request.user)
    
    context = {
        'purchase': purchase,
    }
    return render(request, 'shoppingCard/purchase_detail.html', context)

@login_required
def checkout_detail(request, checkout_id):
    """Display details of a specific checkout"""
    checkout = get_object_or_404(Checkout, checkout_id=checkout_id, user=request.user)
    
    context = {
        'checkout': checkout,
        'purchases': checkout.products.all(),
    }
    return render(request, 'shoppingCard/checkout_detail.html', context)
