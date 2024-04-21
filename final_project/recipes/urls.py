from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.recipe_list, name="recipe_list"),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add_recipe/', views.add_recipe, name="add_recipe"),
    path('delete/<int:id>', views.delete_recipe, name="delete_recipe"),
]
