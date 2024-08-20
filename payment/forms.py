from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Full Name'}), required=True)
    shipping_email = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),required=True)
    shipping_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bulding Floor Door No'}), required=True)
    shipping_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}), required=True)
    shipping_city = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),required=True)
    shipping_state = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),required=False)
    shipping_pincode = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PinCode'}), required=False)
    shipping_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        # fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city',
        #           'shipping_state', 'shipping_pincode', 'shipping_country']
        exclude=['user',]

class  PaymentForm(forms.Form):
    card_name = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Name on card'}), required=True)
    card_number = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Card Number'}), required=True)
    card_exp_data = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Expire date'}), required=True)
    card_cvv_number = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'cvv code'}), required=True)
    card_address1 = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Billing Address1'}), required=True)
    card_address2 = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Billing Address2'}), required=False)
    card_city = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'billing City'}), required=True)
    card_pincode = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'pincode'}), required=True)
    card_state = forms.CharField(label='', widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required=True)
