from django.contrib import admin
from .models import CustomUser, Profile, CartItem
from category.models import Food


# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display= ["username", "email"]

class ProfileAdmin(admin.ModelAdmin):
    list_display= ["username", "address"]
class CartItemAdmin(admin.ModelAdmin):
    list_display= ["food", "quantity","total_price", "created_at"]
        
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(CartItem)