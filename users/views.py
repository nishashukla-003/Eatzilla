from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CustomForm, CustomLoginForm
from .models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create CustomUser views here.

class CustomUserView(CreateView):
    model = CustomUser
    form_class = CustomForm
    template_name = 'users/signup.html' # HTML template
    success_url =  reverse_lazy("login")    # Redirect after login
    
class UserLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("homepage")
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")  # Redirect to login after logout         
class LogoutPageView( TemplateView):
    template_name = "users/logout.html"
   
    
