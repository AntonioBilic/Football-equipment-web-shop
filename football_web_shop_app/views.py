from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import *


def home(request):
    products = Product.objects.all()
    return render(request, 'web_shop/home.html',{'products': products})







#USER REGISTRATION,LOGIN,LOGOUT
def register_view(request):

    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
         
    data = {
        'form' : form
    }
    
    return render(request,'account/register.html', data)


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password are incorrect')

    return render(request,'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')



def category_list(request):
    categories = Category.objects.all()

    data ={
        'categories': categories  
    }
    return render(request,'web_shop/category_list.html', data)


def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    product_images = product.products_image.all()
    
    data = {
        'product': product,
        'product_images': product_images,
    }

    return render(request, 'web_shop/product_detail.html', data)
