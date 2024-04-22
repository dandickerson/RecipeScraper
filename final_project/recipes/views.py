from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
import requests
from .models import Recipe, Ingredient, RecipeIngredient, RecipeCategory
from .forms import RecipeForm
from django.http import HttpResponseRedirect
from django.template import loader
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class RecipeList(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'


def add_recipe(request):
    if request.method == 'POST':
        recipe_url = request.POST.get('recipe_url', '')
        category_id = request.POST.get('category')
        category = RecipeCategory.objects.get(pk=category_id)
        page = requests.get(recipe_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('h2', {'class': 'tasty-recipes-title'}).text.strip()
        description = soup.find('div', {'class': 'tasty-recipes-description'})
        image = soup.find('img')
        if image:
            src_value = image['src']
            recipe_image = src_value
        if description:
            description = description.text.strip()
        ingredients_list = []
        ingredients_div = soup.find('div', {'class': 'tasty-recipes-ingredients'})

        if ingredients_div:
            ul_element = ingredients_div.find('ul')
            if ul_element:
                list_items = ul_element.find_all('li')

                for li in list_items:
                    ingredient_name = li.get_text()
                    unit = li.get('data-unit')
                    quantity = li.get('data-amount')
                    if quantity:
                        ingredients_list.append((ingredient_name, unit, quantity))
                    else:
                        print(f"No quantity found for ingredient: {ingredient_name}")
            else:
                print('No unordered list found in div')
        else:
            print('Div with class="tasty-recipes-ingredients" not found')

        new_recipe = Recipe.objects.create(title=title, description=description, category=category, recipe_image=recipe_image)

        for ingredient_data in ingredients_list:
            ingredient_name, unit, quantity = ingredient_data  # Unpack tuple
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
            RecipeIngredient.objects.create(
                recipe=new_recipe,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit,
            )

        return render(request, 'recipes/recipe_detail.html', {'recipe': new_recipe})

    else:
        categories = RecipeCategory.objects.all()
        return render(request, 'recipes/add_recipe.html', {'categories': categories})


def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes:recipe_list')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})



