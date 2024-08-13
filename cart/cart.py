from store.models import Product, Profile
import json


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # Get the current session key  if it exists
        # this will throw keyError if 'session_key' not in req.POST
        # so we go for
        cart = self.session.get('session_key')
        # {'1': 3}
        # if the user is new, no session key create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}  # creating new session key assigning value

        # Make sure cart is available on all pages of website
        self.cart = cart

    def maintain_state(self):
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # save carty to profile Model
            current_user.update(old_cart=str(carty))

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            # self.cart[product_id] = {'price': str(product.price)}  # {'1': {'price': '350.00'}}
        self.session.modified = True

        # Deal with logged in user
        self.maintain_state()

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            # self.cart[product_id] = {'price': str(product.price)}  # {'1': {'price': '350.00'}}
        self.session.modified = True

        # Deal with loggedIn user
        self.maintain_state()

    def cart_total(self):
        # get product ids
        products_ids = self.cart.keys()
        # look those key in our product data base model
        products = Product.objects.filter(id__in=products_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids form carts
        product_ids = self.cart.keys()
        # use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)

        # Return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # {'4':3 '2':5}

        ourCart = self.cart
        ourCart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Deleting from cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        self.maintain_state()
