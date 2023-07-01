from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Articles(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(blank=True, verbose_name='Текст статьи')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=True)
    photo = models.ImageField(upload_to='media', blank=True, verbose_name='Фото')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('notes', kwargs={'slug_name' : self.slug})
    
    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
        ordering = ['-time_create', 'title']

    
class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('cat', kwargs={'cats' : self.slug})
    
    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Comments(models.Model):
    articl = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=True)
    text = models.TextField(verbose_name='Текст комментария', null=True)
    is_active = models.BooleanField(default=True, verbose_name='Опубликовать', null=True)
    create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)

    def __str__(self):
        return f'{self.author}'
    
    class Meta:
        verbose_name = 'комментарии'
        verbose_name_plural = 'комментарии'
        ordering = ['id']



