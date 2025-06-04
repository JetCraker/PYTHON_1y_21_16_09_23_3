from django.db import models


class Rubric(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Рубрика')

    def __str__(self):
        return self.name


class Bd(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тема')
    content = models.TextField(verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.rubric.name})"


class GoiTeen(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']
