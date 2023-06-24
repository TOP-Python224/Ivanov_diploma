from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', index, name='home'),
    path('notes/<str:slug_name>/', about, name='notes'),
    path('add/', add_an_article, name='add'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='reg'),
    path('category/<str:cats>/', index, name='cat'),
    path('logout/', logout_user, name='logout'),
    path('my_page/', my_page, name='my_page'),
    path('my_page/<int:id>/', delete_aricles, name='delete_articles'),
    path('del_comm/<int:id>/', del_com, name='del_com'),
]