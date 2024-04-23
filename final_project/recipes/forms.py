import requests
from bs4 import BeautifulSoup
from django import forms
from .models import Recipe, RecipeIngredient
from django.http import HttpResponseRedirect


class RecipeForm(forms.ModelForm):
    recipe_url = forms.URLField(label='Recipe URL')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category',
                  'instructions', 'recipe_image']

