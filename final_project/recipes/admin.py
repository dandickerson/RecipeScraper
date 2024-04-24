from django.contrib import admin
from .models import *


# Register your models here.


admin.site.register(RecipeCategory)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Instruction)
admin.site.register(RecipeInstruction)
