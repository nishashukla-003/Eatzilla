from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    payment_method = forms.ChoiceField(
        choices=[('COD', 'Cash on Delivery'), ('UPI', 'UPI'), ('CARD', 'Card')],
        widget=forms.RadioSelect,
        required=True
    )
    
    
