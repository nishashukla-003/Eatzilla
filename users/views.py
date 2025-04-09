from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import CustomForm, CustomLoginForm, ProfileForm, CartItemForm
from .models import CustomUser, Profile, CartItem, Food
from category.models import Food
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

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
    next_page = reverse_lazy("login")  

class ProfileUpate(UpdateView, LoginRequiredMixin): #LoginRequiredMixin ensures only logged-in users hi page acess kar skta hai.
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy("profile_details")
        
    def get_object(self, queryset=None):  #get_object() retrieves or creates the profile for the logged-in user.
        return Profile.objects.get_or_create(user=self.request.user)[0]

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile_details.html"
    success_url = reverse_lazy("profile_details")

    def get_object(self):
        return Profile.objects.get_or_create(user=self.request.user)[0]
    
# Create CartItem views.

class CartItemCreateView(LoginRequiredMixin,CreateView):
    model = CartItem
    form_class = CartItemForm
    template_name = "users/create_cart.html"
    success_url = reverse_lazy("list_cart")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.price = form.instance.food_item.price 
        form.instance.total_price = form.instance.price * form.instance.quantity
        return super().form_valid(form)
    
    
class CartItemListView(LoginRequiredMixin,ListView):
    model = CartItem
    template_name = "users/list_cart.html"
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user, is_ordered=False)  
class CartItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'users/update_cart.html'
    success_url = reverse_lazy('list_cart')

    def form_valid(self, form):
        form.instance.total_price = form.instance.quantity * form.instance.price
        return super().form_valid(form)

class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = 'users/delete_cart.html'
    success_url = reverse_lazy('list_cart')


def add_to_cart(request, pk):
    if request.method == "GET":
        obj = Food.objects.get(id=pk)
        cart_item = CartItem.objects.get(user=request.user, food_item=obj)
        if cart_item:
            cart_item.quantity+=1
            cart_item.save()
        else:
            CartItem.objects.create(
                user = request.user,
                food_item = obj,
                quantity = 1,
                
            )
        return {"success":True}