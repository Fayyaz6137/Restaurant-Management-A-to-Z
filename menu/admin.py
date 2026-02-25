from django.contrib import admin
from .models import Category, MenuItem, MenuItemIngredient, Ingredient

class MenuItemIngredientInline(admin.TabularInline):
    model = MenuItemIngredient
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [MenuItemIngredientInline]

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(MenuItemIngredient)
admin.site.register(Ingredient)