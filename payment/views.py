from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress
from django.contrib import messages


# Create your views here.
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.cart_total()
        if request.user.is_authenticated:
            # GEt the billing form
            billing_form = PaymentForm()
            return render(request, 'billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'total': total,'shipping_info': request.POST,'billing_form':billing_form})

        else:
            return render(request, 'billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'total': total,'shipping_info': request.POST})
        shipping_form=request.POST
        return render(request, 'billing_info.html',{'cart_products': cart_products, 'quantities': quantities, 'total': total,'shipping_info':shipping_form })
    else:
        messages.error(request, "Access Tonight")
        return redirect('home')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    quantities = cart.get_quants  # {'1': 3}
    total = cart.cart_total()
    cart_products = cart.get_prods

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id or None)
        # checkout  as loggedIn user
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html',
                      {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                       'shipping_form': shipping_form})
    shipping_form = ShippingForm()
    return render(request, 'checkout.html',{'cart_products': cart_products, 'quantities': quantities, 'total': total,'shipping_form': shipping_form})


def payment_success(request):
    return render(request, 'payment_success.html', {})
