from django.contrib import admin
from .models import Category, Food, FoodTopping, ToppingsCustomization

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    
class FoodAdmin(admin.ModelAdmin):
    model = Food
    list_display = ["name", "price"]
class FoodToppingAdmin(admin.ModelAdmin):
    model = FoodTopping

class ToppingsCustomizationAdmin(admin.ModelAdmin):
    model = ToppingsCustomization
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register( FoodTopping, FoodToppingAdmin)
admin.site.register(ToppingsCustomization, ToppingsCustomizationAdmin)