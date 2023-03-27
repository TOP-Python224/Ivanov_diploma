from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


# СДЕЛАТЬ: модели, имеющие отношение к авторизации и аутентификации лучше выносить в отдельное django приложение (см. соответствующую лекцию)
class AdvUser(AbstractUser):
    # КОММЕНТАРИЙ: в модели AbstractUser есть поле is_active — если вы хотите разрешить пользователю авторизацию только по прохождении активации, то лучше после регистрации записать в это поле False, изменив на True по выполнении пользователем необходимых действий для активации
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию')
    send_messages = models.BooleanField(default=True, db_index=True, verbose_name='Присылать уведомления?')

    class Meta:
        pass


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT, verbose_name='Рубрика', null=True)
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    # ИСПРАВИТЬ здесь и далее: согласно налоговому законодательству (приказ от 14 сентября 2020 г. N ЕД-7-20/662@) для хранения и использования денежных величин в информационно-технических системах необходимо использовать числа с фиксированной, а не плавающей точкой
    # ИСПРАВИТЬ: не рекомендую допускать запись в таблицу товарных позиций с отсутствующей, или нулевой, или отрицательной ценой
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена',
    )
    # КОММЕНТАРИЙ: возможно, есть резон хранить историю изменения цен — это можно сделать в отдельной таблице, а значения для полей price и old_price получать запросами
    old_price = models.FloatField(null=True, blank=True, verbose_name='Старая цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата')
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', verbose_name='Фото', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товар'
        verbose_name = 'Товар'
        ordering = ['-published']
        constraints = [
            models.CheckConstraint(
                name='price_gt_zero',
                check=Q(price__gt=0),
            )
        ]


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрика'
        verbose_name = 'Рубрики'
        ordering = ['name']


# ДОБАВИТЬ: модель корзины

