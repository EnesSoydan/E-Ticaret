from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.payment_view, name='payment'),
    path('complete/', views.order_complete, name='order_complete'),
    path('history/', views.order_history, name='order_history'),
]