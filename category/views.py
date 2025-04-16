from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import FoodForm, ContactMessageForm
from .models import Food, ContactMessage

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

class Home(LoginRequiredMixin, TemplateView):
    template_name = "category/home_page.html"
    permission_classes = []
    
    
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['object_list'] = Food.objects.all()
        context['user'] = self.request.user
        return context

def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form to create a new ContactMessage entry
            # Optional: Add email sending or flash message here
            return redirect('contact_thank_you')  # Redirect to a thank-you page
    else:
        form = ContactMessageForm()

    context = {
        'form': form
    }
    return render(request, 'category/Contact_us.html', context)

def contact_thank_you(request):
    return render(request, 'category/contact_thank_you.html')

def terms_of_service_view(request):
    return render(request, 'category/terms_of_service.html')

def privacy_policy_view(request):
    return render(request, 'category/privacy_policy.html')