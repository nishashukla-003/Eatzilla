from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


#create Signup field
class CustomForm(UserCreationForm):
    username = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"class": "forms-control"}),
        help_text="",
    )
    password1 = forms.CharField(
        max_length=10, label= "password", 
        widget= forms.PasswordInput(attrs={"class":"forms-control"}),  #passwordInput - Hashing password in signup page
        help_text = '')
    
    password2 = forms.CharField(
        max_length=10, 
        label= "password confirmation", 
        widget= forms.PasswordInput(attrs={"class":"forms-control"}), 
        help_text = '')

    class Meta:
        model = CustomUser
        fields = [                 # add usefull fields
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",    
        ]
        exclude = (              # exclude extra fields
            "last_login",
            "groups",
            "is_staff",
            "is_active",
            "date_joined",
            "user_permissions",
            "is_superuser",           
             )
               
#Create login 
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
