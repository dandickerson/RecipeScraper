from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
import requests
from .models import Recipe, Ingredient, RecipeIngredient, RecipeCategory
from .forms import RecipeForm
from django.http import HttpResponseRedirect

# Create your views here.


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


# def add_recipe(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             recipe = form.scrape()
#             if recipe:
#                 return redirect('recipe_list')
#     else:
#         form = RecipeForm()
#     return render(request, 'recipes/add_recipe.html', {'form': form})


def add_recipe(request):
    if request.method == 'POST':
        recipe_url = request.POST.get('recipe_url', '')
        category_id = request.POST.get('category')
        category = RecipeCategory.objects.get(pk=category_id)
        page = requests.get(recipe_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('h2', {'class': 'tasty-recipes-title'}).text.strip()
        description = soup.find('div', {'class': 'tasty-recipes-description'})
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
                    # Check if quantity exists before assigning it
                    if quantity:
                        ingredients_list.append((ingredient_name, unit, quantity))
                    else:
                        # Handle the case where quantity is not available
                        print(f"No quantity found for ingredient: {ingredient_name}")
            else:
                print('No unordered list found in div')
        else:
            print('Div with class="tasty-recipes-ingredients" not found')

        new_recipe = Recipe.objects.create(title=title, description=description, category=category)

        for ingredient_data in ingredients_list:
            ingredient_name, unit, quantity = ingredient_data  # Unpack tuple
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
            RecipeIngredient.objects.create(
                recipe=new_recipe,
                ingredient=ingredient,
                quantity=quantity,  # Assign the quantity only if it exists
                unit=unit,
            )

        return render(request, 'recipes/recipe_detail.html', {'recipe': new_recipe})

    else:
        categories = RecipeCategory.objects.all()
        context = {'categories': categories}
        return render(request, 'recipes/add_recipe.html', context)



def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')  # Redirect to recipe list page after deleting recipe
    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})
