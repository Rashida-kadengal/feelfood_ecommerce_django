from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from store.forms import ProductReviewForm
from .models import Product, Order, OrderItem, Cart, CartItem,ProductReview
from django.db.models import Q

def home(request):
    products = Product.objects.all() # Get the first 6 products
    return render(request, 'home.html', {'products': products})

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save the contact form data
        # For now, we'll just add a success message
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
        return redirect('contact_us')
    
    return render(request, 'contactus.html')

def about_us(request):
    return render(request, 'aboutus.html')



def product_list(request):
    query = request.GET.get('search', '')  # Get the search query from the request
    products = Product.objects.all()  # Initialize products with all items

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )  # Filter products by name or description 

    context = {
        'products': products,
        'query': query  # Pass the query back to the template to display in the search box
    }
    return render(request, 'product_list.html', context)


def product_detail(request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        reviews=product.product_review.all()
        review_form=ProductReviewForm()
        return render(request, 'product_detail.html', {'product': product,'reviews':reviews,'form':review_form})

def create_product_review(request,product_id):
    if request.method=="POST":
            product = get_object_or_404(Product, pk=product_id)
            review_form=ProductReviewForm(request.POST,request.FILES)
            if review_form.is_valid():
                review=review_form.save(commit=False)
                review.product=product
                review.user=request.user
                if 'product_image' in request.FILES:
                    review.product_image=request.FILES['product_image']
                    review.save()
                return redirect('product_detail',product_id=product.id)
            else:
                reviews=product.product_review.all()
                return render(request, 'product_detail.html', {'product': product,'reviews':reviews,'form':review_form})
    else:
        return redirect('product_detail',product_id=product.id)
    


@login_required
def delete_product_review(request, product_id, review_id):
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(ProductReview, pk=review_id, product=product)

    if review.user == request.user:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this review.")

    return redirect('product_detail', product_id=product.id)


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Get quantity from request, default to 1 if not provided
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if created:
        # If a new cart item, set its quantity
        cart_item.quantity = quantity
    else:
        # If it already exists, add the quantity to the existing quantity
        cart_item.quantity += quantity

    cart_item.save()
    
    return redirect('cart')

@login_required
def buy_now(request, product_id):
    # Get the product to be purchased
    product = get_object_or_404(Product, pk=product_id)
    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    # Create a cart item for the product, or update it if it already exists
    if created:
        # If a new cart item, set its quantity
        cart_item.quantity = quantity
    else:
        # If it already exists, add the quantity to the existing quantity
        cart_item.quantity += quantity

    cart_item.save()

    # Redirect to the checkout page with the current cart
    return redirect('checkout')





@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    # Calculate total price for each cart item and the overall total
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    # Calculate the cart total
    cart_total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        # Process the order
        order = Order.objects.create(user=request.user, total=cart_total)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Clear the cart after creating the order
        cart.items.all().delete()
        return redirect('my_orders')

    return render(request, 'checkout.html', {'cart': cart, 'cart_items': cart_items, 'cart_total': cart_total})




@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')
    return render(request, 'profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})
