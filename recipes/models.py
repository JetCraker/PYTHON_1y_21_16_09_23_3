from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=100)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', null=True, blank=True)
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return self.name



