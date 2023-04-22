from .models import Rubric, Product
from cart.cart import Cart


def context(request):
    context = {}
    context['rubrics'] = Rubric.objects.all()
    return context

def carts(request):
    context = {}
    
    context['cart'] = Cart(request)
    return context