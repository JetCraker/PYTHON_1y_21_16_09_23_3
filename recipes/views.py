from django.forms import modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from .forms import IngredientForm, BaseIngredientFormSet, RecipeForm
from .models import Recipe, Ingredient


def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_ingredients')
    else:
        form = IngredientForm()
    return render(request, 'add_ingredient.html', {'form': form})


IngredientFormSet = modelformset_factory(
    Ingredient,
    formset=BaseIngredientFormSet,
    fields=('name', 'quantity'), extra=1
)


IngredientInlineFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    fields=('name', 'quantity'), extra=2, can_delete=True
)


def edit_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == "POST":
        formset = IngredientInlineFormSet(request.POST, instance=recipe)
        if formset.is_valid():
            formset.save()
            return redirect('recipe_detail', pk=pk)
    else:
        formset = IngredientInlineFormSet(instance=recipe)
    return render(request, 'edit_recipe.html', {'formset': formset, 'recipe': recipe})


def list_ingredients(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'list_ingredients.html',
                  {'ingredients': ingredients})


def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('edit_recipe', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request ,'create_recipe.html', {'form': form})


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})
