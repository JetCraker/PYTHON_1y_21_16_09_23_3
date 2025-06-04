from django.contrib import admin
from .models import Rubric, Bd


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Bd)
class BdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rubric', 'created_at')
