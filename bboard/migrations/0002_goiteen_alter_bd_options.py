# Generated by Django 5.1.6 on 2025-05-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoiTeen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('published', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
        migrations.AlterModelOptions(
            name='bd',
            options={'ordering': ['-created_at']},
        ),
    ]
