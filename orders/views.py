from django.shortcuts import render,redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# Create your views here.

def payment_view(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total = quantity * product.price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total,
        })
        total_price += total

    return render(request, 'orders/payment.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def order_complete(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    total_price = 0
    for product in products:
        quantity = cart[str(product.id)]
        total_price += product.price * quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        is_paid=True  # Simüle ediyoruz, gerçek ödeme entegrasyonunda bu False olabilir
    )

    for product in products:
        quantity = cart[str(product.id)]
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            item_price=product.price
        )

    # Sepeti temizle
    request.session['cart'] = {}

    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})