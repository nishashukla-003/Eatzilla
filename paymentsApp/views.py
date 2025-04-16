import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Payment
from users.models import CartItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
@login_required
def create_checkout_session(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user, is_ordered=False)
    total = sum(item.total_price for item in cart_items)

    if total == 0:
        return render(request, 'payment/error.html', {'message': 'Cart is empty!'})
    amount_in_paise = int(total * 100)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Food Order',
                },
                'unit_amount': amount_in_paise,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/payment/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://localhost:8000/payment/cancel/',
    )
    Payment.objects.create(
        user=user,
        method='CARD',
        amount=total,  
        transaction_id=session.id,
        success=False,
    )
    return redirect(session.url, code=303)

def payment_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    payment = Payment.objects.filter(transaction_id=session_id).first()
    if payment:
        payment.success = True
        payment.save()

        # 🧹 Optional: Mark cart items as ordered
        CartItem.objects.filter(user=payment.user, is_ordered=False).update(is_ordered=True)

    return render(request, 'payment/success.html', {'payment': payment})

def payment_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    payment = Payment.objects.filter(transaction_id=session_id).first()
    if payment:
        payment.success = True
        payment.save()

    return render(request, 'payment/success.html', {'payment': payment})

def payment_cancel(request):
    return render(request, 'payment/cancel.html')
    