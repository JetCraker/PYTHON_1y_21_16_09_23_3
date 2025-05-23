# Generated by Django 5.1.6 on 2025-04-13 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0002_author_category_order_book_product_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Назва рубрики', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введіть назву запчастини', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GoITeen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введіть заголовок оголошення', max_length=100)),
                ('content', models.TextField(help_text='Введіть текст оголошення')),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='Вкажіть ціну оголошення', max_digits=8)),
                ('rubric', models.ForeignKey(help_text='Вкажіть рубрику для цього оголошення', on_delete=django.db.models.deletion.CASCADE, to='Market.rubric')),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введіть назву машини', max_length=100)),
                ('spares', models.ManyToManyField(blank=True, help_text='Оберіть запчастини які є в цій машині', related_name='machines', to='Market.spare')),
            ],
        ),
    ]
