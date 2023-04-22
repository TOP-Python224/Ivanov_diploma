import json
from django.conf import settings
from catalog.models import Product
from decimal import Decimal



class Cart:
    def __init__(self, request):
        '''Создаем в сессии пустой словарь для карзины с ключем cart'''
        self.session = request.session

        if not self.session.get('cart'):
            self.session['cart'] = {}

        self.cart = self.session.get('cart')
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = {
                
                'title' : product.title,
                'published' : str(product.published),
                'content' : product.content,
                'photo' : str(product.photo.url),
                'id' : product.id
                
            }

        for item in cart.values():
            item ['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        '''Добавление товара в карзину или увеличение его колличества'''
        
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity' : 0,
                                     'price' : str(product.price)}
            
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def clear(self):
        '''Удаляем корзину из сессии '''
        del self.session['cart']

    def save(self):
        '''сохраняем изменения в сессии'''
        self.session.modified = True

    def remove(self, product):
        '''Удаление товара из корзины'''

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
        self.save()