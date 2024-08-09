from django.shortcuts import render
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth.models import User


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
            messages.success(request, "You Have Been Logged In")
            return redirect("home")
        else:
            messages.success(request, "there was an error   please try again")
            return redirect('home')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out.. thanks for stopping by...")
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
            messages.error(request, "Whoops! There Was a problem Registering. Please try again")
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
