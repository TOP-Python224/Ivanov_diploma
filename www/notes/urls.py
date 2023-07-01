from django.urls import path, re_path
from .views import *
from django.views.decorators.cache import cache_page

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', index, name='home'),
    path('notes/<str:slug_name>/', about, name='notes'),
    path('add/', add_an_article, name='add'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', signup, name='reg'),
    path('category/<str:cats>/', index, name='cat'),
    path('logout/', logout_user, name='logout'),
    path('my_page/', my_page, name='my_page'),
    path('my_page/<int:id>/', delete_aricles, name='delete_articles'),
    path('del_comm/<int:id>/', del_com, name='del_com'),
    path('correct/<int:id>/', correct, name='correct'),
    path('password-reset/', PasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('feedback', feedback, name='feedback')

]


