from django.urls import path
from .views import *


app_name = 'cart'

urlpatterns = [
    path('<int:product_id>', cart_add, name='cart_add'),
    path('', cart, name='carts'),
    path('remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('order', order, name='order'),
]