from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .models import *

from django.views.generic import View
from django.http import JsonResponse


def index(request, rubric=0):
    
    if rubric:
        product = Product.objects.filter(rubric_id=rubric)
        return render(request, 'catalog/index.html', {'product' : product})
    
    product = Product.objects.all()
    return render(request, 'catalog/index.html', {'product' : product})

def other_page(request, page):
    way = f'catalog/{page}.html'
    return render(request, way)

def product(request, id):
    obj = Product.objects.get(pk=id)
    return render(request, 'catalog/product.html', {'obj' : obj})

@login_required
def payment(request):
    return render(request, 'catalog/payment.html')

def feedback(request):
    return render(request, 'catalog/feedback.html')

@login_required
def profile(request):
    cart = Basket.objects.filter(name=request.user.username)
    print(cart)
    return render(request, 'catalog/profile.html', {'bascet' : cart})


class ShopLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'catalog/login.html'


class ShopLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'catalog/logout.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'catalog/registration.html'
    
    success_url = reverse_lazy('catalog:login')


def catalog_list(request):
    search_list = request.GET.get('search', '')
    if search_list:
        product = Product.objects.filter(title__icontains=search_list)
    else:
        product = Product.objects.all()

    return render(request, 'catalog/index.html', {'product' : product})

def messages(request):
    mes = Messages()
    mes.name = request.GET.get('name')
    mes.email = request.GET.get('email')
    mes.messages = request.GET.get('text')
    mes.save()
    return render(request, 'catalog/feedback.html')










