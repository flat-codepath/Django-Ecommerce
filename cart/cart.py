class Cart():
    def __init__(self,request):
        self.session =request.session
        #Get the current session key  if it exists
        # this will throw keyError if 'session_key' not in req.POST
        # so we go for
        cart = self.session.get('session_key')
        # if the user is new, no session key create one!
        if 'session_key' not in request.session:
            cart =self.session['session_key']={} #creating new session key assigning value


        # Make sure cart is available on all pages of website
        self.cart=cart

    def add(self, product):
        product_id = str(product.id)
        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]={'price':str(product.price)} #{'1': {'price': '350.00'}}
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

