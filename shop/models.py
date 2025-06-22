from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Stuff(models.Model):
    stuff_id = models.AutoField(primary_key=True)
    stuff_name = models.CharField(max_length=50)
    stuff_desc= models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='stuffs/', blank=True, null=True, verbose_name='Зображення')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stuff_name

    def average_rating(self):
        ratings = self.rating.all()
        if ratings:
            return sum([rating.stars for rating in ratings]) / len(ratings)
        return 0

class Rating(models.Model):
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="rating")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг товару')
    comment = models.TextField(blank=True, verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('stuff', 'user')


    def __str__(self):
        return f'{self.stuff.stuff_name} - {self.stars} зірочок'


class Bucket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Додано')

    class Meta:
        unique_together = ('user', 'stuff')
        verbose_name = 'Кошик'

    def get_total_price(self):
        return self.stuff.price * self.count

    def __str__(self):
        return f'{self.user.username} - {self.stuff.stuff_name} ({self.count})'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('canceled', 'Скасовано')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Загальна ціна')
    shipping_address = models.TextField(verbose_name='Адреса доставки', blank=True)

    class Meta:
        verbose_name = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення {self.id}, від {self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Замовлення')
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Кількість')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна за одиницю')

    class Meta:
        verbose_name = 'Товар для замовлення'

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.stuff.stuff_name} x {self.quantity}'
