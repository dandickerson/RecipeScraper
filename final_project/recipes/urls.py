from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.RecipeList.as_view(), name="recipe_list"),
    path('<int:pk>/', views.RecipeDetail.as_view(), name='detail'),
    path('add_recipe/', views.add_recipe, name="add_recipe"),
    path('delete/<int:pk>', views.delete_recipe, name="delete_recipe"),
    path('edit/<int:pk>/', views.RecipeUpdateView.as_view(), name='edit_recipe'),
]
