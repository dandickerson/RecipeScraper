from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
import requests
from .models import *
from .forms import RecipeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import re


class RecipeList(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['instructions'] = Instruction.objects.filter(recipe=recipe)
        context['ingredients'] = Ingredient.objects.filter(recipe=recipe)
        context['recipe_ingredients'] = RecipeIngredient.objects.filter(recipe=recipe)
        context['recipe_instructions'] = RecipeInstruction.objects.filter(recipe=recipe)
        return context


def add_recipe(request):
    if request.method == 'POST':
        recipe_url = request.POST.get('recipe_url')
        category_id = request.POST.get('category')
        category = RecipeCategory.objects.get(pk=category_id)
        print(category)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Extract Recipe object fields
        response = requests.get(recipe_url, headers=headers)
        response.raise_for_status()
        page = response.content
        soup = BeautifulSoup(page, 'html.parser')
        title_element = soup.find('h2') # , {'class': 'tasty-recipes-title'})
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Untitled Recipe"
        print(title)
        description = soup.find('div', {'class': 'tasty-recipes-description'})
        image = soup.find('img')
        if image:
            recipe_image = image['src']
        else:
            recipe_image = Recipe.Meta.get_field('recipe_image').get_default()

        # Extract ingredients
        ingredients_list = []
        ingredients_div = soup.find('div', {'class': 'tasty-recipes-ingredients'})
        if ingredients_div:
            ul_element = ingredients_div.find('ul')
            if ul_element:
                list_items = ul_element.find_all('li')
            else:
                print('no unordered list found')
        else:
            print('no div found')

        for li in list_items:
            ingredient_name = li.get_text().strip()
            #check db for existing ingredient
            existing_ingredient = Ingredient.objects.filter(name=ingredient_name).first()
            if existing_ingredient:
                ingredient = existing_ingredient
            else:
                ingredient = Ingredient.objects.create(name=ingredient_name)
            print(ingredient)

            ingredients_list.append((ingredient))

        # Extract Instructions
        instructions_list = []
        instructions_div = soup.find('div', {'class': 'tasty-recipes-instructions'})

        ol_element = instructions_div.find('ol')
        ordered_list_items = ol_element.find_all('li')

        for li in ordered_list_items:
            instruction = li.get_text().strip()
            instruction_object = Instruction.objects.create(instruction=instruction)
            print(instruction)
            instructions_list.append(instruction_object)

        # Create the Recipe object
        new_recipe = Recipe.objects.create(
            title=title,
            description=description.text.strip() if description else '',
            category=category,
            recipe_image=recipe_image
        )

        # create instruction objects
        recipe_instructions = []
        for instruction in instructions_list:
            recipe_instruction = RecipeInstruction.objects.create(
                recipe=new_recipe,
                instruction=instruction
            )
            print(recipe_instruction.instruction)
            recipe_instructions.append(recipe_instruction)

        # Create RecipeIngredient objects for each ingredient
        recipe_ingredients = []
        for ingredient in ingredients_list:
            recipe_ingredient = RecipeIngredient.objects.create(
                recipe=new_recipe,
                ingredient=ingredient
            )
            print(ingredient.name)
            recipe_ingredients.append(recipe_ingredient)
        print('new recipe object created')

        return render(request, 'recipes/recipe_detail.html', {'recipe': new_recipe,
                                                              'recipe_ingredients': recipe_ingredients,
                                                              'recipe_instructions': recipe_instructions})

    else:
        categories = RecipeCategory.objects.all()
        return render(request, 'recipes/add_recipe.html', {'categories': categories})


def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        print('recipe deleted')
        return redirect('recipes:recipe_list')
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})


def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    categories = RecipeCategory.objects.all()

    form = RecipeForm(request.POST or None, instance=recipe)

    if form.is_valid():
        form.save()
        return redirect('recipes:recipe_detail', pk=recipe.pk)

    return render(request, 'recipes/edit_recipe.html', {'form': form, 'categories': categories})
