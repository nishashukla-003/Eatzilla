from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('food/', views.FoodcreateView.as_view(), name= "food" ),
  path('food_list/', views.FoodListView.as_view(), name= "food_list" ),
  path('food_details/<int:pk>/', views.FoodListDetails.as_view(), name= "food_details" ),
  path('food_update/<int:pk>/', views.FoodListUdate.as_view(), name= "food_update" ),
  path('food_delete/<int:pk>/', views.FoodDelete.as_view(), name= "food_delete" ),
  path("home/", views.Home.as_view(), name ="homepage"),
  path('contact/', views.contact_view, name='contact'),
  path('contact/thank-you/', views.contact_thank_you, name='contact_thank_you'),
  path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
  path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
  
]
  

