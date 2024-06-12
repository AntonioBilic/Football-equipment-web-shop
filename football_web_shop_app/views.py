from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegistrationForm,UserLoginForm,ProductReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import *
from django.template.context_processors import csrf


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    data ={
        'categories': categories,
        'products': products
    }
    
    return render(request, 'web_shop/home.html',data)







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
            return redirect('home')
        else:
            messages.info(request, 'Username or Password are incorrect')

    return render(request,'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


#PRODUCT
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    product_images = product.products_image.all()  # Assuming you have a related name 'products_image' for ProductImages
    all_sizes = Size.objects.all()
    reviews = ProductReview.objects.filter(product=product)
    
    if request.method == "POST":
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', id=id)
    else:
        review_form = ProductReviewForm()

    return render(request, 'web_shop/product_detail.html', {
        'product': product,
        'product_images': product_images,
        'all_sizes': all_sizes,
        'reviews': reviews,
        'review_form': review_form,
    })

#ADD ORDER,ORDER DETAIL

def order_detail(request):
    order = Order.objects.filter(user=request.user, paid_status=False).first()
    return render(request, 'web_shop/order_detail.html', {'order': order})

def add_to_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, paid_status=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'product': product, 'price': product.price, 'quantity': 1})
    
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    # Update the order total price
    order.price = sum(item.total_price  for item in order.items.all())
    order.save()
    
    return redirect('order_detail')




def remove_from_order(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order = order_item.order
    order_item.delete()
    return redirect('home')

def update_order_item_quantity(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            order_item.quantity = int(quantity)
            order_item.save()
            
            # Update the order total price
            order_item.order.price = sum(item.total_price for item in order_item.order.items.all())
            order_item.order.save()
    
    return redirect('order_detail')

