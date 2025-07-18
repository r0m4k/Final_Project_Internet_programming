from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json

from landing.models import Teacher

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
