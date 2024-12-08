from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Customer(models.Model):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30
    )
    second_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=20
    )

    def __str__(self):
        return self.first_name + ' ' + self.second_name + ' ' + self.phone_number

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'Покупатели'


class MyUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='myuser_set',  # Уникальное имя
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='myuser_set',  # Уникальное имя
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Product(models.Model):
    title = models.CharField(verbose_name='Товар', max_length=50)
    category = models.CharField(verbose_name='Категория', max_length=50)
    sub_category = models.CharField(verbose_name='Подкатегория',max_length=50)
    text = models.TextField(
        verbose_name='Доп. информация',
        default='Дополнительная информация отсутствует.'
    ) 

    class Meta:
        db_table = 'retail_product'

    def __str__(self):
        return  self.category + '-' + self.sub_category + ': ' + self.title


class Wholesale(models.Model):
    order_date = models.DateTimeField(verbose_name='Дата заказа',)
    region = models.CharField(verbose_name='Регион', max_length=50)
    sales = models.IntegerField(verbose_name='Цена')
    customer = models.ForeignKey(
        Customer,
        verbose_name='Покупатель',
        on_delete=models.RESTRICT
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.RESTRICT
    )

    class Meta:
        db_table = 'retail_wholesale'