from django.db import models
from django.contrib.auth.models import User


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Album(models.Model):
    artist = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    release_date = models.DateField()
    num_stars = models.IntegerField()


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    birthdate = models.DateField()
    age = models.IntegerField()
    mail = models.EmailField()


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Автор")
    surname = models.CharField(max_length=100, verbose_name="Прізвище")


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва книги")
    author = models.ManyToManyField(Author, verbose_name="Автор")
    published_date = models.DateField(verbose_name="Дата публікації")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна",
                                help_text='Можливо ввести не ціле число')

    def __str__(self):
        return f"{self.title} by {self.author}"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'n', "Новий"
        PROGRESSING = 'p', "В обробці"
        COMPLETED = 'c', 'Завершений'
        CANCELLED = 'x', 'Скасований'

    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.NEW,
                              verbose_name="Статус замовлення")


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва категорії")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва продукту")
    description = models.TextField(verbose_name="Опис продукту")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    available = models.BooleanField(default=True, verbose_name="Наявність")
    release_date = models.DateField(verbose_name="Дата завозу", null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категорія')

    def save(self, *args, **kwargs):
        if self.price <= 0:
            raise ValueError("Ціна має бути більшою за нуль!")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Користувач')
    bio = models.TextField(verbose_name='Біографія', blank=True)

    def __str__(self):
        return self.user.name


class Rubric(models.Model):
    name = models.CharField(max_length=50, help_text='Назва рубрики')

    def __str__(self):
        return self.name


class GoITeen(models.Model):
    title = models.CharField(max_length=100, help_text='Введіть заголовок оголошення')
    content = models.TextField(help_text='Введіть текст оголошення')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text='Вкажіть ціну оголошення')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, help_text='Вкажіть рубрику для цього оголошення') \

    def __str__(self):
        return self.title


class Spare(models.Model):
    name = models.CharField(max_length=100, help_text='Введіть назву запчастини')

    def __str__(self):
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=100, help_text='Введіть назву машини')
    spares = models.ManyToManyField(Spare,
                                    blank=True,
                                    related_name='machines',
                                    help_text='Оберіть запчастини які є в цій машині')

    def __str__(self):
        return self.name


class Product2(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва продукту")
    description = models.TextField(verbose_name="Опис продукту", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.name


class Order2(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('completed', 'Завершено'),
        ('canceled', 'Скасовано'),
    ]

    product = models.ForeignKey(
        Product2,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Продукт"
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Кількість",
        blank=True
    )

    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Замовлення {self.id} на продукт {self.product.name}"

