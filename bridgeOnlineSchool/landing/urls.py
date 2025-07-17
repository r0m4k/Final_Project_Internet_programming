from django.urls import path
from . import views

app_name = 'landing' 

urlpatterns = [
    path("", views.home, name="home"),
    path("teachers/<int:pk>", views.teacher, name="teacher"),
]