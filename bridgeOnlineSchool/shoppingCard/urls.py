from django.urls import path
from . import views

app_name = 'shoppingCard'

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add/<int:teacher_id>/', views.add_to_cart, name='add_to_cart'),
    path('count/', views.get_cart_count, name='cart_count'),  # Kept for compatibility
] 