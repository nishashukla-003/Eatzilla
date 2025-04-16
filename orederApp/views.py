from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, DetailView
from .models import Order, OrderItem
from users.models import CartItem, Profile
from .forms import CheckoutForm  # create this form with address and payment_method
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm

    def get_cart_items(self):
        return CartItem.objects.filter(user=self.request.user, is_ordered=False)

    def get_profile_address(self):
        return Profile.objects.get(user=self.request.user).address

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_cart_items()
        address = self.get_profile_address()
        sub_total = sum(item.total_price for item in cart_items)
        discount = Decimal('0.00')
        tax_rate = Decimal('0.18')
        taxes = round(sub_total * tax_rate, 2)
        grand_total = sub_total + taxes - discount
        context.update({
            'cart_items': cart_items,
            'address': address,
            'sub_total': sub_total,
            'discount': discount,
            'taxes': taxes,
            'grand_total': grand_total,
        })
        return context

    def form_valid(self, form):
        cart_items = self.get_cart_items()
        sub_total = sum(item.total_price for item in cart_items)
        discount = 0
        taxes = round(sub_total * 0.18, 2)
        grand_total = round(sub_total + taxes - discount, 2)

        order = Order.objects.create(
            user=self.request.user,
            address=form.cleaned_data['address'],
            sub_total=sub_total,
            discount=discount,
            taxes=taxes,
            grand_total=grand_total,
            payment_method=form.cleaned_data['payment_method'],
            is_paid=False
        )
        order.cart_items.set(cart_items)
         # ✅ Save Order ID to session
        self.request.session['order_id'] = order.id
        # cart_items.delete()  # clear cart after order

        return redirect('order_success', order_id=order.id)

class OrderSuccessView(DetailView):
    model = Order
    template_name = 'order/order_success.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    
# class AddressUda(DetailView):
#     model = Order
#     template_name = 'order/order_success.html'
#     context_object_name = 'order'
#     pk_url_kwarg = 'order_id'
    