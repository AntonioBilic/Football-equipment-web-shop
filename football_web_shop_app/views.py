from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages

def home(request):
    return render(request,'web_shop/index.html')


#USER REGISTRATION AND LOGIN
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
            return redirect('home')
        else:
            messages.info(request, 'Username or Password are incorrect')

    return render(request,'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')