from django.contrib import admin
from django.urls import path
from .views import CheckoutView, OrderSuccessView


urlpatterns = [
    # path('orders/', order_list_view, name='order_list'),
    path('orders/', CheckoutView.as_view(), name='order_list'),
   path('success/<int:order_id>/', OrderSuccessView.as_view(), name='order_success')
    
    
]
