from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    quantities = cart.get_quants  # {'1': 3}
    total =cart.cart_total()
    cart_products = cart.get_prods
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities,'total':total})


def cart_add(request):
    # GET the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in a DB
        product = get_object_or_404(Product, id=product_id)

        # save to session
        cart.add(product=product, quantity=product_qty)
        # Get Cart Quantity
        cart_quantity = cart.__len__()
        messages.success(request,'Product added to Cart')
        response = JsonResponse({'qty': cart_quantity})

        # return response
        # response=JsonResponse({'Product Name:' :product.name })

        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        print(product_id,'-----------------------')
        cart.delete(product=product_id)
        response =JsonResponse({'product': product_id})
        messages.error(request,'Items  Deleted from Shopping Cart')
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request,'Your Cart has been updated')
        return response
