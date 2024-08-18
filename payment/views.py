from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress


# Create your views here.
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
    return render(request, 'checkout.html',
                  {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                   'shipping_form': shipping_form})


def payment_success(request):
    return render(request, 'payment_success.html', {})

