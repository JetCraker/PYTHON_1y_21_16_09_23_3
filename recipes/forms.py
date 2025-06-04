from django import forms
from .models import Ingredient, Recipe
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

        #exclude = ['quantity']


class BaseIngredientFormSet(BaseFormSet):
    def clean(self):
        super().clean()
        names = []

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                name = form.cleaned_data['name']
                if name in names:
                    raise ValidationError('Ігредієнти не можуть повторюватись')
                names.append(name)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title']
