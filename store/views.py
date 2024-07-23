from django.shortcuts import render
from .models import  Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import  SignUpForm
# Create your views here.


def product(request,pk):
    product =Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})








def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{"products":products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "you Have Been  Logged In")
            return redirect("home")
        else:
            messages.success(request, "there was an error   please try again")
            return redirect('home')
    else:
       return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out.. thanks for stopping by...")
    return redirect('home')



def register_user(request):
    if request.method =="POST":
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username =form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #log in user
            user =authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You Have Registered Successfully ")
            return redirect('home')
        else:
            messages.error(request,"Whoops! There Was a problem Registering. Please try again")
            return redirect('register')
    form=SignUpForm()
    return  render(request,'register.html',{'form':form})

