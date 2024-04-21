from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', blank=True)
    instructions = models.TextField(blank=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE, blank=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    unit = models.CharField(max_length=20, blank=True)

