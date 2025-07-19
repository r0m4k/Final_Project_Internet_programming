from django.urls import path
from . import views

app_name = 'shoppingCard'

urlpatterns = [
    # Cart views
    path('', views.view_cart, name='cart'),
    path('add/<int:teacher_id>/', views.add_to_cart, name='add_to_cart'),
    path('count/', views.get_cart_count, name='cart_count'),  # Kept for compatibility
    
    # Checkout views
    path('checkout/', views.checkout_form, name='checkout_form'),
    path('checkout/create/', views.create_checkout, name='create_checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/<uuid:checkout_id>/', views.checkout_detail, name='checkout_detail'),
    
    # Purchase views
    path('purchases/', views.my_purchases, name='my_purchases'),
    path('purchase/<uuid:purchase_id>/', views.purchase_detail, name='purchase_detail'),
] 