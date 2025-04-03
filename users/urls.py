from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.CustomUserView.as_view(), name = 'signup'),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.LogoutPageView.as_view(), name="logout"),
    path("logout_page/", views.UserLogoutView.as_view(), name="logout_page"),
]
