from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import CustomForm, CustomLoginForm, ProfileForm, CartItemForm, UserUpdateForm
from .models import CustomUser, Profile, CartItem, WishlistItem
from category.models import Food
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Sum

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

#Update profile view
class ProfileUpate(UpdateView, LoginRequiredMixin): #LoginRequiredMixin ensures only logged-in users hi page acess kar skta hai.
    model = Profile
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy("profile_details")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = context.get('user_form') or UserUpdateForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        profile_form = self.get_form()
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(
                form=profile_form,
                user_form=user_form
            )) 

    def get_object(self, queryset=None):  #get_object() retrieves or creates the profile for the logged-in user.
        return Profile.objects.get_or_create(user=self.request.user)[0]

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile_details.html"
    success_url = reverse_lazy("profile")

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
    
    
class CartItemListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "users/list_cart.html"
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user, is_ordered=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']
        total_price = sum(item.total_price for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)
        context['total_price'] = total_price
        context['total_quantity'] = total_quantity
        return context
class CartItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'users/update_cart.html'
    success_url = reverse_lazy('list_cart')

    def post(self, request, *args, **kwargs):
        instance = CartItem.objects.get(pk=kwargs.get('pk'))
        act = kwargs.get("act")
        if act=="increase":
            instance.quantity =  instance.quantity + 1
        elif act=="decrease":
            instance.quantity =  instance.quantity - 1
        elif act=="remove":
            CartItem.objects.filter(id=instance.id).delete()
            price = CartItem.objects.filter(user=request.user).aggregate(Sum("total_price"))
            return JsonResponse({"success": True, "deleted":True, "price":price['total_price__sum']})
        else:
            return JsonResponse({"error":"invalid action"})
        instance.total_price = instance.quantity * instance.price
        instance.save()
        price = CartItem.objects.filter(user=request.user).aggregate(Sum("total_price"))
        ctx = {
            "success": True, 
            "quantity":instance.quantity, 
            "price":price['total_price__sum'],
            "total_price": instance.total_price
        }
        return JsonResponse(ctx)
class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = 'users/delete_cart.html'
    success_url = reverse_lazy('list_cart')


def add_to_cart(request, pk):
    if request.method == "GET":
        obj = Food.objects.get(id=pk)
        cart_item, _ = CartItem.objects.get_or_create(
            user = request.user,
            food_item = obj,
            price = obj.price,
            total_price = obj.price,
            is_ordered = False
            )
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(
                user = request.user,
                food_item = obj,
                quantity = 1,
                
            )
        return JsonResponse({"success":True})
    
# wish list view here
class WishlistListView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = 'users/wish_list.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

class WishlistAddView(LoginRequiredMixin, View):
    def get(self, request, food_id):
        food = get_object_or_404(Food, id=food_id)
        WishlistItem.objects.get_or_create(user=request.user, food_item=food)
        return redirect('view_wishlist')

class WishlistRemoveView(LoginRequiredMixin, View):
    def get(self, request, food_id):
        item = WishlistItem.objects.filter(user=request.user, food_item_id=food_id)
        if item.exists():
            item.delete()
        return redirect('view_wishlist')
    
    
