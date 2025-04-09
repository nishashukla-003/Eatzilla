from django.db import models
from django.contrib.auth.models import AbstractUser
from category.models import Food
# Create your models here.

class CustomUser(AbstractUser):
    phone = models.IntegerField(null=True, blank=True) #consider blank value with data base 
    
    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food_item = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        return self.quantity * self.food_item.price


    def __str__(self):
        return f"{self.quantity} {self.food_item.name} by {self.user.username}"

