from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, OrderItem, Order
from django.contrib import messages
from store.models import Product,Profile
import datetime


# Create your views here.

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:

        # Get the order
        order = Order.objects.get(id=pk)

        # Get the Order items
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            # Check if ture or false
            if status == "true":
                # Get the order
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(shipped=False, date_shipped=now)
            messages.success(request, 'Shipping  Status Updated')
            return redirect('home')

        return render(request, 'orders.html', {'order': order, 'items': items})


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the Order
            order = Order.objects.filter(id=num)
            # Grab date time
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, 'Shipping  Status Updated')
            return redirect('home')
        return render(request, 'not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # Get the Order
            order = Order.objects.filter(id=num)
            # Grab date time
            now = datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request, 'Shipping  Status Updated')
            return redirect('home')
        return render(request, 'shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def Process_order(request):
    if request.POST:
        # Get The Cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.cart_total()

        #  Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = total

        # Creating shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n {my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_pincode']}\n{my_shipping['shipping_state']}"

        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()

            # Add Order  Items
            # Get the order ID
            order_id = create_order.pk
            # Get the product info
            for product in cart_products:
                # Get Product ID
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # create_order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
                                                      quantity=value, price=price)
                        create_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                print(key)
                if key == "session_key":
                    # Delete the session key
                    del request.session[key]

            # Delete Cart from Database.(old_cart filed)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart  in database(old_cart field)
            current_user.update(old_cart="")


            messages.success(request, 'Order Placed')
            return redirect('home')

        else:
            # not loggedIn
            # Create an Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()
            # Add Order  Items
            # Get the order ID
            order_id = create_order.pk
            # Get the product info
            for product in cart_products:
                # Get Product ID
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # create_order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value,
                                                      price=price)
                        create_order_item.save()
            # Delete cart items
            for key in list(request.session.keys()):

                if key == "session_key":
                    del request.session[key]


            messages.success(request, 'Order placed')
            return redirect('home')
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.cart_total()
        if request.user.is_authenticated:

            # Create a session with shipping info
            my_shipping = request.POST
            request.session['my_shipping'] = my_shipping

            # GEt the billing form
            billing_form = PaymentForm()
            return render(request, 'billing_info.html',
                          {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                           'shipping_info': request.POST, 'billing_form': billing_form})

        else:

            # Create a session with shipping info
            my_shipping = request.POST
            request.session['my_shipping'] = my_shipping

            billing_form = PaymentForm()
            return render(request, 'billing_info.html',
                          {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                           'shipping_info': request.POST, 'billing_form': billing_form})
    else:
        messages.error(request, "Access Denied")
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
    return render(request, 'checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                                             'shipping_form': shipping_form})


def payment_success(request):
    return render(request, 'payment_success.html', {})

