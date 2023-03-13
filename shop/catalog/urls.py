from django.urls import path




from .views import *

app_name = 'catalog'

urlpatterns = [
    path('', index, name='index'),
    path('<str:page>', other_page, name='other'),
    path('accounts/payment/', payment, name='payment'),
    path('feedback/', feedback, name='feedback'),
    path('accounts/login/', ShopLoginView.as_view(), name='login'),
    path('accounts/logout/', ShopLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
]


