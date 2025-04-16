from django.contrib import admin
from .models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = [ "user", " method", "amount", "success", "transaction_id"]
    
admin.site.register(Payment)