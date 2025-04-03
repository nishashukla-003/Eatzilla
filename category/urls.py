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
  
]
