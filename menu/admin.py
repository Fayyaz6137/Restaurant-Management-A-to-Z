from django.contrib import admin
from .models import Category, MenuItem, MenuItemIngredient, Ingredient

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(MenuItemIngredient)
admin.site.register(Ingredient)