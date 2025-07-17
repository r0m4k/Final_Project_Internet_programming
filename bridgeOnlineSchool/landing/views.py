from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Teacher  # Import your Teacher model

# Create your views here.

def home(request):
    teachers = Teacher.objects.all()  # Get all teachers from database
    context = {
        'teachers': teachers
    }
    return render(request, "landing/index.html", context)

def teacher(request, pk):
    teacher = Teacher.objects.get(id=pk)  # Get all teachers from database
    context = {
        'teacher': teacher
    }
    return render(request, "landing/teacher.html", context)
