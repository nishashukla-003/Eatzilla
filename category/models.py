from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  #this field requred unique value and not blank
  
    def __str__(self):
        return self.name


class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(default="", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True)
    image = models.ImageField(upload_to="food_images/", blank=True, null=True)
    is_available = models.BooleanField(default=True)


class ToppingsCustomization(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class FoodTopping(models.Model):

    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="toppings")
    topping = models.ForeignKey(ToppingsCustomization, on_delete=models.CASCADE)

