from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Teacher, Rating  # Import your Teacher and Rating models

# Create your views here.

def home(request):
    # Start with all teachers
    teachers = Teacher.objects.all()
    pending_teachers = Teacher.objects.filter(is_active=False)  # Get pending teachers
    
    # Apply filters to active teachers only
    active_teachers = Teacher.objects.filter(is_active=True)
    
    # Filter by name (search)
    search_query = request.GET.get('search', '')
    if search_query:
        from django.db.models import Value, CharField
        from django.db.models.functions import Concat
        
        # Search in first name, last name, and full name (first + last)
        active_teachers = active_teachers.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField())
        ).filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )
    
    # Filter by minimum teaching years
    min_years = request.GET.get('min_years', '')
    
    if min_years:
        try:
            min_years = int(min_years)
            active_teachers = active_teachers.filter(teaching_years__gte=min_years)
        except ValueError:
            pass
    
    # Sort by price
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        active_teachers = active_teachers.order_by('lesson_price')
    elif sort_by == 'price_desc':
        active_teachers = active_teachers.order_by('-lesson_price')
    
    # Update teachers queryset to include filtered active teachers and all inactive teachers
    teachers = active_teachers.union(Teacher.objects.filter(is_active=False), all=True)
    
    context = {
        'teachers': teachers,
        'pending_teachers': pending_teachers,
        'search_query': search_query,
        'min_years': min_years,
        'sort_by': sort_by,
        'active_teachers': active_teachers,
    }
    return render(request, "landing/index.html", context)

def teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    
    # If teacher is inactive, only allow staff members to access
    if not teacher.is_active and not request.user.is_staff:
        raise Http404("Teacher not found")
    
    # Get all reviews for this teacher
    reviews = Rating.objects.filter(teacher=teacher).order_by('-created_at')
    
    # Calculate average rating
    avg_rating = 0
    if reviews.exists():
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    # Check if current user has already reviewed this teacher
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Rating.objects.filter(teacher=teacher, user=request.user).exists()
    
    context = {
        'teacher': teacher,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'reviews_count': reviews.count(),
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, "landing/teacher.html", context)

@staff_member_required
def approve_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.is_active = True
    teacher.save()
    return redirect('landing:home')

@staff_member_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher_name = f'{teacher.first_name} {teacher.last_name}'
    teacher.delete()
    return redirect('landing:home')

@staff_member_required
def deactivate_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.is_active = False
    teacher.save()
    messages.success(request, f'Teacher {teacher.first_name} {teacher.last_name} has been deactivated and moved to pending.')
    return redirect('landing:home')

@login_required
def add_review(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        
        # Validate rating
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid rating value.'})
            messages.error(request, 'Invalid rating value.')
            return redirect('landing:teacher', pk=teacher_id)
        
        # Check if user already reviewed this teacher
        existing_review = Rating.objects.filter(teacher=teacher, user=request.user).first()
        
        if existing_review:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'You have already reviewed this teacher.'})
            messages.warning(request, 'You have already reviewed this teacher.')
        else:
            # Create new review
            try:
                Rating.objects.create(
                    teacher=teacher,
                    user=request.user,
                    rating=int(rating),
                    description=description
                )
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Your review has been submitted successfully!'})
                messages.success(request, 'Your review has been submitted successfully!')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'An error occurred while submitting your review.'})
                messages.error(request, 'An error occurred while submitting your review.')
    
    return redirect('landing:teacher', pk=teacher_id)

@staff_member_required
def delete_review(request, review_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)
    review = get_object_or_404(Rating, id=review_id)
    teacher_id = review.teacher.id
    try:
        review.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Review deleted successfully.'})
        messages.success(request, 'Review deleted successfully.')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'An error occurred while deleting the review.'})
        messages.error(request, 'An error occurred while deleting the review.')
    return redirect('landing:teacher', pk=teacher_id)
