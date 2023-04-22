from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .cart import Cart
from catalog.models import Product, Basket
from django.http import JsonResponse
# Create your views here.

def cart_add(request, product_id):
    
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('catalog:index')

def cart(request):
    prod = Cart(request) 
    
    if prod:
        return render(request, 'cart/cart.html', {"prod" : prod})
    else:
        return render(request, 'catalog/payment.html')
    

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:carts')

def order(request):
    b = Basket()
    cart = Cart(request)
    
    b.name = request.user.username
    b.total_price = cart.get_total_price()
    b.save()
    cart.clear()
   
   
    return render(request, 'cart/all.html')

