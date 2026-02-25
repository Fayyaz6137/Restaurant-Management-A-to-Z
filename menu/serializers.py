from rest_framework import serializers
from .models import Category, MenuItem, Ingredient, MenuItemIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class MenuItemIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = MenuItemIngredient
        fields = ["ingredient", "quantity_required"]


class MenuItemSerializer(serializers.ModelSerializer):
    ingredients_detail = MenuItemIngredientSerializer(
        source="menuitemingredient_set", many=True, read_only=True
    )
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "category_name", "price", "is_available", "ingredients_detail"]


class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "items"]