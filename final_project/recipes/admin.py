from django.contrib import admin
from .models import RecipeCategory, Ingredient, Recipe, RecipeIngredient


# Register your models here.


admin.site.register(RecipeCategory)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
