from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)


class Instruction(models.Model):
    instruction = models.CharField(max_length=300)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', blank=True)
    instructions = models.ManyToManyField(Instruction, through='RecipeInstruction', blank=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE, blank=True)
    recipe_image = models.CharField(max_length=500, default='https://t4.ftcdn.net/jpg/02/15/28/55/360_F_215285525_fqG9SPnXZfOrwFxHzqI6d1hHPVmdSUSx.jpg')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE)
