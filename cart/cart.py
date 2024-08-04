from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get the current session key  if it exists
        # this will throw keyError if 'session_key' not in req.POST
        # so we go for
        cart = self.session.get('session_key')
        # if the user is new, no session key create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}  # creating new session key assigning value

        # Make sure cart is available on all pages of website
        self.cart = cart

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
        quantities=self.cart
        return quantities
        pass
