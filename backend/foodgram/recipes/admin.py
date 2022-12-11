from django.contrib import admin

from .models import Favorite, Ingredients, Recipes, Tag, IngredientInRecipe, ShoppingCart, RecipeTag

admin.site.register(Tag)
admin.site.register(Ingredients)
admin.site.register(Recipes)
admin.site.register(Favorite)
admin.site.register(IngredientInRecipe)
admin.site.register(ShoppingCart)
admin.site.register(RecipeTag)
