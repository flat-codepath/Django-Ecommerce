from django.shortcuts import render
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

# Create your views here.
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summery.html', {"categories": categories})


def category(request, foo):
    # replace hyphens with space
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        # look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})

    except:
        messages.error(request, "That category Doesn't Exist")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get there saved cart from the database
            saved_cart = current_user.old_cart  # {"4": 2, "5": 2, "1": 2, "8": 2}
            # convert database  string to python dictionary
            if saved_cart:
                # converting to dictionary Using JSON
                converted_cart = json.loads(saved_cart)  # {'4': 2, '5': 2, '1': 2, '8': 2}

                # add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # let's loop thru the dictionary and add the items  from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, "You Have Been Logged In")
            return redirect("home")
        else:
            messages.success(request, "there was an error   please try again")
            return redirect('home')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out.. thanks for stopping by...")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Registered Successfully ")
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('register')
    form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        # current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            login(request, request.user)
            messages.success(request, 'User Has Been Updated!!')
            return redirect('home')
        for error in list(user_form.errors.values()):
            messages.error(request, error)
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'You Must Be logged In')
        return render('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they  fill out the form
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                # when user logged  in successfully by default the user details would be there in
                # session  but if you are changing the password means  the password change value should be updated through session
                update_session_auth_hash(request, form.user)
                messages.success(request, "Your Password has Been Updated Please Login Again")
                logout(request)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(request.user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You Must be logged In')
        form = ChangePasswordForm(request.user)
    return render(request, 'update_password.html', {'form': form})


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current  User's shipping address
        shipping_user = ShippingAddress.objects.get(id=request.user.id)
        # Get original User  Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get  user's  Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # save the Original form
            form.save()
            # save the shipping form
            shipping_form.save()
            messages.success(request, 'Your Info Has Been Updated!!')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'You Must Be logged In')
        return render('home')


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # query The Products DB models
        searched = Product.objects.filter(Q(name__icontains=searched) or Q(description__icontaions=searched))
        # Test for null
        if not searched:
            messages.error(request, 'That products in not Exists... please try again')
        return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
