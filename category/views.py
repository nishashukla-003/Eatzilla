from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import FoodForm
from .models import Food

# Create your views here.
#Create Category 
class FoodcreateView(CreateView):
    model = Food
    form_class =FoodForm
    template_name = "category/food_create.html"
    success_url = reverse_lazy('food_list')

#food List
class FoodListView(ListView):
    model = Food
    template_name = "category/food_list.html"
    success_url = reverse_lazy('food_details')

    
# food details
class FoodListDetails(DetailView):
    model = Food
    template_name = "category/food_details.html"
    
# food update
class FoodListUdate(UpdateView):
    model = Food
    form_class =FoodForm
    template_name = "category/food_update.html"
    success_url = reverse_lazy('food_list')
    
# food delete 
class FoodDelete(DeleteView):
    model = Food
    template_name = "category/food_delete.html"
    success_url = reverse_lazy('food_list')
    
    
class Home(TemplateView):
    template_name = "category/home_page.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['object_list'] = Food.objects.all()
        return context
