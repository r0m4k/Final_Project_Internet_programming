from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Teacher, Rating


def home(request):
    """
    Renders the home page with filtered teacher listings.
    
    Handles teacher search, filtering by experience, reviews, and sorting.
    Supports both active teachers for public view and pending teachers for staff.
    
    Args:
        request: HTTP request object containing GET parameters for filtering
        
    Returns:
        HttpResponse: Rendered home page template with teacher data
    """
    # Initialize teacher querysets with rating annotations
    teachers = Teacher.objects.all()
    pending_teachers = Teacher.objects.filter(is_active=False).annotate(avg_rating=Avg('ratings__rating'))
    active_teachers = Teacher.objects.filter(is_active=True).annotate(avg_rating=Avg('ratings__rating'))
    
    # Apply search filter for teacher names
    search_query = request.GET.get('search', '')
    if search_query:
        from django.db.models import Value, CharField
        from django.db.models.functions import Concat
        
        # Enable search across first name, last name, and concatenated full name
        active_teachers = active_teachers.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name', output_field=CharField())
        ).filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )
    
    # Apply experience filter based on minimum teaching years
    min_years = request.GET.get('min_years', '')
    if min_years:
        try:
            min_years = int(min_years)
            active_teachers = active_teachers.filter(teaching_years__gte=min_years)
        except ValueError:
            # Silently ignore invalid input to maintain user experience
            pass
    
    # Filter to include only teachers with existing reviews
    has_reviews = request.GET.get('has_reviews', '')
    if has_reviews:
        active_teachers = active_teachers.filter(ratings__isnull=False).distinct()
    
    # Apply price-based sorting options
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        active_teachers = active_teachers.order_by('lesson_price')
    elif sort_by == 'price_desc':
        active_teachers = active_teachers.order_by('-lesson_price')
    
    # Update teachers queryset to include filtered active teachers and all inactive teachers
    teachers = active_teachers.union(Teacher.objects.filter(is_active=False), all=True)
    
    context = {
        'teachers': teachers,
        'active_teachers': active_teachers,
        'pending_teachers': pending_teachers,
        'search_query': search_query,
        'min_years': min_years,
        'sort_by': sort_by,
        'has_reviews': has_reviews,
    }
    
    return render(request, "landing/index.html", context)

def teacher(request, pk):
    """
    Displays detailed teacher profile page with reviews and rating functionality.
    
    Restricts access to inactive teacher profiles for non-staff users.
    Calculates average rating and determines if current user has already reviewed the teacher.
    
    Args:
        request: HTTP request object
        pk: Primary key of the teacher to display
        
    Returns:
        HttpResponse: Rendered teacher detail page template
        
    Raises:
        Http404: If teacher is inactive and user is not staff
    """
    teacher = get_object_or_404(Teacher, id=pk)
    
    # Restrict access to inactive teacher profiles for non-staff users
    if not teacher.is_active and not request.user.is_staff:
        raise Http404("Teacher not found")
    
    # Retrieve all reviews for this teacher, ordered by creation date
    reviews = Rating.objects.filter(teacher=teacher).order_by('-created_at')
    
    # Calculate average rating from all reviews
    avg_rating = 0
    if reviews.exists():
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    # Determine if current authenticated user has already submitted a review
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
    """
    Activates a pending teacher profile, making it visible to public users.
    
    Args:
        request: HTTP request object
        pk: Primary key of the teacher to approve
        
    Returns:
        HttpResponse: Redirect to home page
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.is_active = True
    teacher.save()
    return redirect('landing:home')

@staff_member_required
def delete_teacher(request, pk):
    """
    Permanently removes a teacher profile from the system.
    
    Args:
        request: HTTP request object
        pk: Primary key of the teacher to delete
        
    Returns:
        HttpResponse: Redirect to home page
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher_name = f'{teacher.first_name} {teacher.last_name}'
    teacher.delete()
    return redirect('landing:home')

@staff_member_required
def deactivate_teacher(request, pk):
    """
    Deactivates an active teacher profile, moving it to pending status.
    
    Args:
        request: HTTP request object
        pk: Primary key of the teacher to deactivate
        
    Returns:
        HttpResponse: Redirect to home page with success message
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.is_active = False
    teacher.save()
    return redirect('landing:home')

@login_required
def add_review(request, teacher_id):
    """
    Handles the submission of teacher reviews by authenticated users.
    
    Validates rating input, prevents duplicate reviews, and supports both AJAX and standard form submissions.
    Only allows one review per user per teacher to maintain review integrity.
    
    Args:
        request: HTTP request object
        teacher_id: ID of the teacher being reviewed
        
    Returns:
        JsonResponse: For AJAX requests with success/error status
        HttpResponse: Redirect to teacher page for standard requests
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        
        # Validate rating input within acceptable range
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Invalid rating value.'})
            messages.error(request, 'Invalid rating value.')
            return redirect('landing:teacher', pk=teacher_id)
        
        # Prevent duplicate reviews from the same user
        existing_review = Rating.objects.filter(teacher=teacher, user=request.user).first()
        
        if existing_review:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'You have already reviewed this teacher.'})
            messages.warning(request, 'You have already reviewed this teacher.')
        else:
            # Create and save new review record
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
    """
    Removes a teacher review from the system (staff only).
    
    Supports both AJAX and standard HTTP requests for deletion operations.
    Only accepts POST requests for security purposes.
    
    Args:
        request: HTTP request object
        review_id: ID of the review to delete
        
    Returns:
        JsonResponse: For AJAX requests with success/error status
        HttpResponse: Redirect to teacher page for standard requests
    """
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

def about_us(request):
    """
    Renders the About Us page containing organizational information and mission statement.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered about us page template
    """
    return render(request, 'landing/about_us.html')

def contact(request):
    """
    Renders the Contact page with organizational contact information and inquiry form.
    
    Args:
        request: HTTP request object
        
    Returns:
        HttpResponse: Rendered contact page template
    """
    return render(request, 'landing/contact.html')
