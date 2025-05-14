from django.shortcuts import render,redirect
from products.models import Product
# Create your views here.

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    # Ürün varsa adedini arttır
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('/products/')

def view_cart(request):
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

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')