# Bridge Online School

## 0. Application Specif Accounts for testing
- **Admin Account**
  - Username: admin
  - Password: Admin12345!
- **Staff Account**
  - Username: staff_1
  - Password: Staff12345!
- **General User Account**
  - Username: user_1
  - Password: User12345!

## 1. Project Description

Bridge Online School is a dynamic web platform that connects bridge instructors with students seeking personalized bridge lessons. The platform serves as a marketplace where qualified teachers can register, create profiles, and offer their expertise to students worldwide.

### Core Concept
- **Teacher Registration**: New bridge instructors can register and create detailed profiles showcasing their expertise, experience, and pricing
- **Student Discovery**: Students can browse teacher profiles, read reviews, and book lessons based on their preferences
- **Admin Oversight**: Administrative staff can review and approve teacher profiles before they become publicly visible
- **E-commerce Integration**: Complete shopping cart and checkout system for lesson purchases

### Key Features
- Teacher profile management with avatar uploads
- Student review and rating system (1-5 stars)
- Advanced filtering and search functionality
- Shopping cart with localStorage persistence
- Secure checkout and purchase tracking
- Admin panel for teacher approval and management

## 2. Web Project Structure

### User Types and Access Levels

#### **Public Users (Unauthenticated)**
- **Home Page** (`/`): Browse active teachers, search, filter, and view teacher profiles
- **About Us** (`/about-us/`): Platform information and mission
- **Contact** (`/contact/`): Contact form and company information
- **Teacher Profiles** (`/teachers/<id>`): View teacher details, reviews, and lesson information
- **Shopping Cart** (`/cart/`): Add teachers to cart, manage quantities, proceed to checkout

#### **Registered Users**
- **Profile Management** (`/authentication/profile/`): Account settings, password changes
- **Checkout** (`/cart/checkout/`): Complete lesson purchases with payment processing
- **Checkout success** (`/cart/checkout/success`): Invoice after the "payment" processing
- **Profile Settings Managment** (`/authentication/profile/`): Create and manage profiles

#### **Administrative Staff**
- **Teacher Approval** (`/admin/approve-teacher/<id>/`): Activate pending teacher profiles
- **Teacher Management** (`/admin/deactivate-teacher/<id>/`, `/admin/delete-teacher/<id>/`): Manage teacher status
- **Review Moderation** (`/admin/delete-review/<id>/`): Remove inappropriate reviews
- **Pending Teachers Section**: Dedicated area on home page for managing pending applications

### Page Interconnection Flow

```
Home Page (/) 
├── Teacher Profiles → Individual teacher pages
├── Search/Filter → Filtered teacher listings
├── Admin Section → Pending teachers management (staff only)
└── Navigation → About, Contact, Authentication

Authentication (/authentication/)
├── Login → Profile page or redirect to intended page
├── Register → Profile page with welcome message
├── Forgot Password → Email-based password reset
└── Profile → Account settings + Teacher profile creation

Shopping Cart (/cart/)
├── Add to Cart → Teacher profile pages
├── Cart Management → Quantity updates, item removal
├── Checkout → Payment processing and purchase creation
└── Purchase History → Order tracking and status
```

## 3. Database Structure and Models

### Core Models

#### **Teacher Model** (`landing/models.py`)
```python
class Teacher(models.Model):
    user = models.OneToOneField(User, related_name='teacher_profile', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    experience = models.CharField(max_length=500)
    teaching_years = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='teachers/avatars')
    lesson_price = models.DecimalField(max_digits=6, decimal_places=0)
    course_price = models.DecimalField(max_digits=7, decimal_places=0)
    is_active = models.BooleanField(default=False)  # Admin approval required
```

**Functionality:**
- Links to Django User model for authentication
- Stores professional information and pricing
- `is_active` field controls public visibility (admin approval system)
- Avatar uploads stored in `media/teachers/avatars/`

#### **Rating Model** (`landing/models.py`)
```python
class Rating(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('teacher', 'user')  # One review per user per teacher
```

**Functionality:**
- Enforces one review per user per teacher through database constraint
- 1-5 star rating system with optional text descriptions
- Timestamp tracking for review history

#### **Purchase Model** (`shoppingCard/models.py`)
```python
class Purchase(models.Model):
    purchase_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    teacher_profile = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lesson_purchases')
    number_of_lessons = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    communication_method = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
```

**Functionality:**
- UUID-based primary keys for security
- Automatic price calculation based on lesson quantity and teacher rate
- Status tracking for lesson fulfillment
- Communication preferences and notes for lesson coordination

#### **Checkout Model** (`shoppingCard/models.py`)
```python
class Checkout(models.Model):
    checkout_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    products = models.ManyToManyField(Purchase, related_name='checkouts', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')
    billing_email = models.EmailField()
    billing_name = models.CharField(max_length=100)
```

**Functionality:**
- Groups multiple purchases into single checkout sessions
- Payment status tracking for financial record-keeping
- Billing information storage for transaction records
- Automatic total calculation from associated purchases

## 4. Technical Documentation: Non-Trivial Features

### Forgot Password Functionality

**Implementation Location:** `authentication/views.py` - `forgot_password()` function

**Technical Process:**
1. **Email Validation**: User submits email address through `ForgotPasswordForm`
2. **User Lookup**: System finds user by email address in Django User model
3. **Temporary Password Generation**: Creates 12-character random password using mixed alphanumeric characters
4. **Password Update**: Updates user's password using Django's `set_password()` method
5. **Email Delivery**: Sends email with temporary password using Django's `send_mail()` function
6. **Security**: Users must change temporary password upon next login

**Code Implementation:**
```python
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generate secure temporary password
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Update user password
            user.set_password(temp_password)
            user.save()
            
            # Send email with temporary password
            send_mail(
                subject='Your Temporary Password - Bridge Online School',
                message=f'Your temporary password is: {temp_password}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect('authentication:login')
```

**Security Features:**
- Random password generation with mixed character types
- Email-based delivery for secure transmission
- Automatic password change requirement
- Django's built-in password hashing

### Shopping Cart Functionality

**Implementation Location:** `static/assets/js/main.js` - `ShoppingCart` class and `shoppingCard/views.py`

**Technical Architecture:**

#### **Client-Side Cart System (JavaScript)**
```javascript
class ShoppingCart {
    constructor() {
        this.storageKey = 'bridgeSchoolCart';
    }
    
    getCart() {
        const cart = localStorage.getItem(this.storageKey);
        return cart ? JSON.parse(cart) : {};
    }
    
    saveCart(cart) {
        localStorage.setItem(this.storageKey, JSON.stringify(cart));
        this.updateNavbarCount();
    }
    
    addItem(teacher) {
        const cart = this.getCart();
        const teacherId = teacher.id.toString();
        
        if (cart[teacherId]) {
            cart[teacherId].quantity += 1;
        } else {
            cart[teacherId] = {
                ...teacher,
                quantity: 1,
                notes: '',
                communication_method: ''
            };
        }
        
        this.saveCart(cart);
    }
}
```

**Features:**
- **localStorage Persistence**: Cart data persists across browser sessions
- **Quantity Management**: Incremental quantity updates for existing items
- **Real-time Updates**: Navbar cart count updates automatically
- **Guest User Support**: Works for non-authenticated users

#### **Server-Side Processing (Django Views)**
```python
@login_required
@require_POST
def create_checkout(request):
    try:
        data = json.loads(request.body)
        
        # Create checkout record
        checkout = Checkout.objects.create(
            user=request.user,
            total_amount=Decimal(str(data['total_amount'])),
            billing_email=data.get('billing_email', request.user.email),
            billing_name=data.get('billing_name', request.user.get_full_name()),
            payment_method=data.get('payment_method', 'credit_card'),
            payment_status='completed'
        )
        
        # Process individual purchases
        for item in data['items']:
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
        
        return JsonResponse({
            'success': True,
            'checkout_id': str(checkout.checkout_id)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error creating checkout: {str(e)}'
        })
```

**Key Features:**
- **Atomic Operations**: Database transactions ensure data consistency
- **Error Handling**: Comprehensive error management with rollback capabilities
- **JSON Processing**: Client-side cart data converted to server-side models
- **Payment Integration**: Ready for payment processor integration
- **Purchase Tracking**: Individual lesson purchases with status tracking

#### **Cart-User Integration**
```javascript
// Handle pending checkout for users who logged in after adding items to cart
function proceedToCheckout() {
    if (!isAuthenticated) {
        const cartItems = window.shoppingCart.getCart();
        localStorage.setItem('pendingCheckout', JSON.stringify(cartItems));
        window.location.href = '/authentication/login/';
        return;
    }
    // Continue with checkout process
}
```

**Features:**
- **Guest-to-Authenticated Flow**: Cart data preserved when users log in
- **Pending Checkout**: Unfinished checkouts saved for later completion
- **Seamless UX**: No cart data loss during authentication process

---

### Other Functionality Features

#### **Teacher Approval System**
- Teachers register with `is_active=False`
- Admin reviews profiles in pending section
- Approval changes `is_active=True` for public visibility
- Deactivation moves teachers back to pending status

#### **Review System Integrity**
- Database constraint ensures one review per user per teacher
- Star rating system (1-5) with optional text descriptions
- Admin moderation capabilities for inappropriate content

#### **Responsive Design**
- Bootstrap-based responsive layout
- Mobile-first navigation with hamburger menu
- Progressive enhancement with jQuery
- AOS (Animate On Scroll) for enhanced UX

#### **Security Implementation**
- CSRF protection on all forms
- Login required decorators for protected views
- Staff member required decorators for admin functions
- Password complexity validation
- Session management with automatic logout

---

**Technology Stack:**
- **Backend**: Django 4.x with Python 3.x
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **Database**: SQLite (development), PostgreSQL ready
- **Styling**: Bootstrap 5.x with custom CSS
- **File Storage**: Django's media file handling
- **Email**: Django's email backend
- **Authentication**: Django's built-in user system
