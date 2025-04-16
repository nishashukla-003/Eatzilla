from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["user","order_date", "total_price", "status" ]

# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ["order","product_name", "quantity", "unit_price" ]
    
admin.site.register(Order)
admin.site.register(OrderItem)


