import requests
from bs4 import BeautifulSoup
from django import forms
from .models import Recipe, Ingredient, Instruction
from django.http import HttpResponseRedirect


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'recipe_image']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['instruction']
