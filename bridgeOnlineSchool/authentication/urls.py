from django.urls import path
from . import views

app_name = 'authentication' 

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.profile_view, name='profile'),
]