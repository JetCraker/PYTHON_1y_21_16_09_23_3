from django.urls import path
from . import views


urlpatterns = [
    path('', views.add_ingredient, name='add_ingredient'),

    path('ingredints', views.list_ingredients, name='list_ingredients'),
    path('ingredints/add/', views.add_ingredient, name='add_ingredient'),
    path('<int:pk>/edit_recipe', views.edit_recipe, name='edit_recipe'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail')
]
