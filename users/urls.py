from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.CustomUserView.as_view(), name = 'signup'),
    path("login/", views.UserLoginView.as_view(), name="login"),
    # path("logout/", views.LogoutPageView.as_view(), name="logout"),
    path("logout_page/", views.UserLogoutView.as_view(), name="logout_page"),
    path("profile/", views.ProfileUpate.as_view(), name="profile"),
    path("profile_details/", views.ProfileDetailView.as_view(), name="profile_details"),
    path("create_cart/", views.CartItemCreateView.as_view(), name="create_cart"),
    path("list_cart/", views.CartItemListView.as_view(), name="list_cart"),
    path('cart/update/<int:pk>/<str:act>/', views.CartItemUpdateView.as_view(), name='update_cart'),
    path('cart/delete/<int:pk>/', views.CartItemDeleteView.as_view(), name='delete_cart'),
    path('add-to-cart/<int:pk>/',views.add_to_cart, name="add_to_cart"),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart_from_detail'),
    
    path('wishlist/', views.WishlistListView.as_view(), name='view_wishlist'),
    path('wishlist/add/<int:food_id>/', views.WishlistAddView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:food_id>/', views.WishlistRemoveView.as_view(), name='remove_from_wishlist'),
  

]
