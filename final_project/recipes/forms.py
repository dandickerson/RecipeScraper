import requests
from bs4 import BeautifulSoup
from django import forms
from .models import Recipe, RecipeIngredient
from django.http import HttpResponseRedirect


class RecipeForm(forms.ModelForm):
    recipe_url = forms.URLField(label='Recipe URL')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'category',
                  'instructions']

    # def scrape(self):
    #     recipe_url = self.cleaned_data['recipe_url']
    #     response = requests.get(recipe_url)
    #     if response.status_code == 200:
    #         print(response.text)
    #         try:
    #             soup = BeautifulSoup(response.text, 'html.parser')
    #             title = soup.find('h2', {'class': 'tasty-recipes-title'}).text.strip()
    #             print("Title: ", title)
    #             description = soup.find('div', {'class': 'tasty-recipes-description'})
    #             # Loop through ingredients by finding all <li> possibly. Creating each ingredient object.
    #             # Add more fields...
    #             recipe = Recipe(title=title, description=description, ingredients='spaghetti', category='dinner', prep_time='',
    #                             cook_time='', servings='', instructions='')
    #             recipe.save()
    #             return recipe
    #         except Exception as e:
    #             print("Error during scraping:", e)
    #             return None
    #     else:
    #         raise ValueError('Failed to fetch recipe data from URL')
