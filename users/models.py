from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    phone = models.IntegerField(null=True, blank=True) #consider blank value with data base 
    
    def __str__(self):
        return self.username


