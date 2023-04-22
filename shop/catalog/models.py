from django.db import models
from django.contrib.auth.models import AbstractUser


 

class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата')
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', verbose_name='Фото', null=True)
    old_price = models.FloatField(null=True, blank=True, verbose_name='Старая цена')
    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT, verbose_name='Рубрика', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товар'
        verbose_name = 'Товар'
        ordering = ['-published']

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название', default='1')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрика'
        verbose_name = 'Рубрики'
        ordering = ['name']


class Basket(models.Model):
    name = models.CharField(max_length=20)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Корзина'
        verbose_name = 'Корзина'
        ordering = ['name']


class Messages(models.Model):
    name = models.CharField(max_length=20)
    messages = models.TextField(null=True, blank=True, verbose_name='Сообщение')
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Сообщение'
        verbose_name = 'Сообщение'
        ordering = ['name']







