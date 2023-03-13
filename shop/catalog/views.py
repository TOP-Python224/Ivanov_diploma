from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):
    product = Product.objects.all()
    return render(request, 'catalog/index.html', {'product' : product})

def other_page(request, page):
    way = f'catalog/{page}.html'
    return render(request, way)

@login_required
def payment(request):
    return render(request, 'catalog/payment.html')

def feedback(request):
    return render(request, 'catalog/feedback.html')

@login_required
def profile(request):
    return render(request, 'catalog/profile.html')


class ShopLoginView(LoginView):
    template_name = 'catalog/login.html'

class ShopLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'catalog/logout.html'