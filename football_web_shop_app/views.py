from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import UserRegistrationForm,UserLoginForm,ProductReviewForm,EditProfileForm,ShippingAddressForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import *
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator



stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    
    query = request.GET.get('query', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    color = request.GET.get('color', '')
    brand_id = request.GET.get('brand')
    size_id = request.GET.get('size')
    category_id = request.GET.get('category_id')
    subcategory_id = request.GET.get('subcategory_id')
    category_name = "All Products"

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        category_name = f"All Products in {category.name}"
    elif subcategory_id:
        subcategory = get_object_or_404(Category, id=subcategory_id)
        products = Product.objects.filter(category=subcategory)
        category_name = f"All Products in {subcategory.name}"
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()




    products = Product.objects.all()
    categories = Category.objects.filter(parent=None)
    brands = Brand.objects.all()
    sizes = Size.objects.all()

    # Filtering based on the query parameters
    if query:
        products = products.filter(name__icontains=query)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if color:
        products = products.filter(color__icontains=color)
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if size_id:
        products = products.filter(sizes__id=size_id)
    if subcategory_id:
        products = products.filter(category__id=subcategory_id)
    if category_id:
        subcategories = Category.objects.filter(parent_id=category_id)
        products = products.filter(category__in=subcategories) | products.filter(category__id=category_id)

     # Implementing pagination
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'sizes': sizes,
        'selected_category': category_id,
        'selected_subcategory': subcategory_id,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'color': color,
        'brand_id': brand_id,
        'size_id': size_id,
        'page_obj': page_obj,
        'category_name': category_name,
    }

    return render(request, 'web_shop/home.html', context)


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

@login_required
def user_settings(request):
    return render(request, 'account/settings.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'form': form})

#PRODUCT

def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    product_images = product.products_image.all()  # Assuming you have a related name 'products_image' for ProductImages
    sizes = Product.objects.all()
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
        'all_sizes': sizes,
        'reviews': reviews,
        'review_form': review_form,
    })

#ADD ORDER,ORDER DETAIL

def order_detail(request):
    order = Order.objects.filter(user=request.user, paid_status=False).first()
    return render(request, 'web_shop/order_detail.html', {'order': order})


@login_required(login_url='login')
def add_to_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        size_id = request.POST.get('size')
        size = get_object_or_404(Size, id=size_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Get or create the order for the user
        order, created = Order.objects.get_or_create(user=request.user, paid_status=False)
        
        # Get or create the order item for the specified product and size
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            size=size,
            defaults={'price': product.price, 'quantity': quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        # Update the order total price
        order.price = sum(item.quantity * item.price for item in order.items.all())
        order.save()
        
        return redirect('home')  

    return render(request, 'web_shop/product_detail.html', {'product': product, 'sizes': product.sizes.all()})


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


@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        messages.info(request, f'{product.name} is already in your wishlist.')
    else:
        messages.success(request, f'{product.name} has been added to your wishlist.')

    return redirect('home')


@login_required(login_url='login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'web_shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')



@login_required(login_url='login')
def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            
            order = get_object_or_404(Order, user=request.user, paid_status=False)
            order.shipping_address = shipping_address
            order.save()
            
            messages.success(request, 'Shipping address added successfully!')
            return redirect('order_detail')
    else:
        form = ShippingAddressForm()
    
    return render(request, 'web_shop/add_shipping_address.html', {'form': form})

#STRIPE PAYMENT 
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_0b11aa4927da37524bcce755bff6e2d70269865223ab74225fc3242b3c74cc57'

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']

        # Fulfill the purchase
        order_id = payment_intent.get('metadata', {}).get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            
            order.paid_status = True
            order.save()

            # Clear the cart (delete order items)
            OrderItem.objects.filter(order=order).delete()

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
       

    return HttpResponse(status=200)

def create_checkout_session(request):
    order = get_object_or_404(Order, user=request.user, paid_status=False)
    if not order.shipping_address:
        messages.error(request, 'Please add a shipping address before proceeding to payment.')
        return redirect('add_shipping_address')
      
    domain_url = 'http://localhost:8000/'
    total = int(order.total_price * 100)  # Convert to cents

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order Total',
                        },
                        'unit_amount': total,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain_url + 'success/',
            cancel_url=domain_url + 'cancel/',
            metadata={
                'order_id': order.id  # Pass the order ID to the webhook
            }
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f'Error creating Stripe checkout session: {str(e)}')
        return redirect('order_detail')


def success_view(request):
    return render(request, 'web_shop/success.html')

def cancel_view(request):
    return render(request, 'web_shop/cancel.html')