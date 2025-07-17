from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from landing.models import Teacher
import re

class SignUpForm(UserCreationForm):
	email = forms.EmailField(
		label="", 
		widget=forms.EmailInput(attrs={
			'class':'form-control', 
			'placeholder':'Email Address',
			'required': True
		})
	)
	first_name = forms.CharField(
		label="", 
		max_length=100, 
		widget=forms.TextInput(attrs={
			'class':'form-control', 
			'placeholder':'First Name',
			'required': True
		})
	)
	last_name = forms.CharField(
		label="", 
		max_length=100, 
		widget=forms.TextInput(attrs={
			'class':'form-control', 
			'placeholder':'Last Name',
			'required': True
		})
	)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].widget.attrs['required'] = True
		self.fields['username'].widget.attrs['maxlength'] = 50
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 50 characters or fewer. Letters, digits and _ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].widget.attrs['required'] = True
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Must contain at least 8 characters.</li><li>Must include letters, numbers, and special characters.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].widget.attrs['required'] = True
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("A user with that email already exists.")
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if len(username) > 50:
			raise forms.ValidationError("Username must be 50 characters or fewer.")
		if not re.match(r'^[a-zA-Z0-9_]+$', username):
			raise forms.ValidationError("Username can only contain letters, digits, and underscores.")
		return username

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name')
		if not first_name:
			raise forms.ValidationError("First name is required.")
		if not re.match(r'^[a-zA-Z\s]+$', first_name):
			raise forms.ValidationError("First name can only contain letters.")
		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name')
		if not last_name:
			raise forms.ValidationError("Last name is required.")
		if not re.match(r'^[a-zA-Z\s]+$', last_name):
			raise forms.ValidationError("Last name can only contain letters.")
		return last_name

	def clean_password1(self):
		password1 = self.cleaned_data.get('password1')
		if len(password1) < 8:
			raise forms.ValidationError("Password must be at least 8 characters long.")
		
		# Check for letters, numbers, and special characters
		has_letter = re.search(r'[a-zA-Z]', password1)
		has_digit = re.search(r'\d', password1)
		has_special = re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password1)
		
		if not (has_letter and has_digit and has_special):
			raise forms.ValidationError("Password must contain letters, numbers, and special characters.")
		
		return password1
	
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
	
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match.")

		return password2

# Form for forgot password functionality
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="", 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your email address',
            'required': True
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email address.")
        return email

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['title', 'experience', 'teaching_years', 'avatar', 'lesson_price', 'course_price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., World Champion, Respectful Educator, European Champion',
                'maxlength': 50
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your teaching experience and qualifications...',
                'rows': 4,
                'maxlength': 500
            }),
            'teaching_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of teaching experience',
                'min': 0,
                'max': 99
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'lesson_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per lesson (USD)',
                'min': 0,
                'max': 999999,
                'step': 1
            }),
            'course_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per course (USD)',
                'min': 0,
                'max': 9999999,
                'step': 1
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title is required.")
        if len(title) > 50:
            raise forms.ValidationError("Title must be 50 characters or fewer.")
        return title
    
    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if not experience:
            raise forms.ValidationError("Experience description is required.")
        if len(experience) > 500:
            raise forms.ValidationError("Experience must be 500 characters or fewer.")
        return experience
    
    def clean_teaching_years(self):
        teaching_years = self.cleaned_data.get('teaching_years')
        if teaching_years is not None and (teaching_years < 0 or teaching_years > 99):
            raise forms.ValidationError("Teaching years must be between 0 and 99.")
        return teaching_years
    
    def clean_lesson_price(self):
        lesson_price = self.cleaned_data.get('lesson_price')
        if lesson_price is None:
            raise forms.ValidationError("Lesson price is required.")
        if lesson_price < 0 or lesson_price > 999999:
            raise forms.ValidationError("Lesson price must be between 0 and 999,999.")
        return lesson_price
    
    def clean_course_price(self):
        course_price = self.cleaned_data.get('course_price')
        if course_price is None:
            raise forms.ValidationError("Course price is required.")
        if course_price < 0 or course_price > 9999999:
            raise forms.ValidationError("Course price must be between 0 and 9,999,999.")
        return course_price