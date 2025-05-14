from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view,home_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', register_view, name='signup'),
    path('payment/', views.payment_view, name='payment'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    
]
