from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def home(request):
    return render(request,'web_shop/index.html')


#USER REGISTRATION AND LOGIN
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"hey {username}, your account was created succesfully")
            new_user = authenticate(username=form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
            login(request, new_user)
        return redirect('home')
    else:
        form = UserRegistrationForm()

    data = {
        'form': form,
    }

    return render(request, 'account/register.html', data)


def login(request):
    if request.user.is_authenticated:
        return render ('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')