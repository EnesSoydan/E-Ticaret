from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CartItem, Product
# Create your views here.


def cart_view(request):
    # Kullanıcının sepetini al
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'account/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def payment_view(request):
    if request.method == 'POST':
        # Ödeme işlemi burada yapılır (örneğin, kart bilgileri vb.)
        # Burada ödeme başarılı olursa, kullanıcıyı ödeme başarılı sayfasına yönlendirebilirsiniz.
        
        # Ödeme başarılı
        messages.success(request, "Ödemeniz başarılı bir şekilde alınmıştır.")
        return redirect('payment_success')  # payment_success URL'sine yönlendir

    return render(request, 'accounts/payment.html')  # Ödeme formunu gösteren sayfa

def payment_success_view(request):
    return render(request, 'accounts/payment_success.html')  # Ödeme başarılı mesajı

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Zaten giriş yaptınız.")
        return redirect('products')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products')
        else:
            # Hatalı girişte kullanıcıya mesaj göster
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', context = {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')