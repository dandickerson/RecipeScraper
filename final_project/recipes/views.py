from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
import requests
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .mixins import RedirectToLoginMixin
from django.db.models import Q
from django.urls import reverse
from random import choice
from django.conf import settings
import os


class RecipeList(RedirectToLoginMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = Recipe.objects.filter(user=self.request.user)
        ingredient_query = self.request.GET.get('ingredient')
        if ingredient_query:
            queryset = queryset.filter(ingredients__name__icontains=ingredient_query)
            return queryset.distinct()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


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
    title = 'Untitled Recipe'
    if request.method == 'POST':
        validator = URLValidator()
        recipe_url = request.POST.get('recipe_url')
        if not recipe_url.startswith(('http://', 'https://')):
            recipe_url = 'http://' + recipe_url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(recipe_url, headers=headers)
            response.raise_for_status()
            page = response.content
            soup = BeautifulSoup(page, 'html.parser')
        except requests.RequestException:
            error_message = "URL is not reachable. Please enter a valid URL."
            return render(request, 'recipes/error.html', {'error_message': error_message})

        try:
            validator(recipe_url)
        except ValidationError:
            error_message = "Invalid URL. Please enter a valid URL."
            render(request, 'recipes/error.html', {'error_message': error_message})

        category_id = request.POST.get('category')
        category = RecipeCategory.objects.get(pk=category_id)
        print(category)

        # Extract Recipe object fields
        main = soup.find('main')
        if not main:
            main = soup.find('body')
        header = main.find_all('div', class_=re.compile('.*header.*'))
        for tag in header:
            if 'recipe' in tag.name:
                head = tag.find(['h1', 'h2'])
                if head:
                    title = head.text.strip()
                    break
            elif tag.name in ['div', 'article']:
                head = tag.find(['h1', 'h2'])
                if head:
                    title = head.text.strip()
                    break
            else:
                title = "Untitled Recipe"
                break

        image = main.find('img')
        recipe_image = image['src']

        # Extract ingredients
        ingredients_list = []
        ingredients_div = soup.find('div', class_=re.compile('.*ingredient.*'))
        if ingredients_div:
            list_items = ingredients_div.find_all('li')
        else:
            error_message = f"Cannot import ingredients"
            return render(request, 'recipes/error.html', {'error_message': error_message})

        for li in list_items:
            ingredient_name = li.get_text().strip()
            existing_ingredient = Ingredient.objects.filter(name=ingredient_name).first()
            if existing_ingredient:
                ingredient = existing_ingredient
            else:
                ingredient = Ingredient.objects.create(name=ingredient_name)
            print(ingredient)

            ingredients_list.append(ingredient)

        # Extract Instructions
        instructions_list = []
        instructions_div = soup.find('div', class_=re.compile('.*instruction.*'))
        if not instructions_div:
            error_message = f"Cannot import instructions"
            return render(request, 'recipes/error.html', {'error_message': error_message})
        instruction_items = instructions_div.find_all('li')
        for item in instruction_items:
            instruction_text = item.get_text().strip()
            instruction = Instruction.objects.create(instruction=instruction_text)
            print(instruction)
            instructions_list.append(instruction)

        # Create the Recipe object
        new_recipe = Recipe.objects.create(
            title=title,
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


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/edit_recipe.html'

    def get_success_url(self):
        return reverse_lazy('recipes:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all()
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return super().form_valid(form)


def random_recipe(request):
    all_recipes = Recipe.objects.all()
    random_recipe = choice(all_recipes)
    return redirect(reverse('recipes:detail', kwargs={'pk': random_recipe.pk}))