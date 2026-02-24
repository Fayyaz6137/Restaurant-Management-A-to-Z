from django.db import models

from django.db import models
from restaurants.models import Branch


class Category(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    class Meta:
        unique_together = ("name", "branch")
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories_per_unit = models.FloatField()

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through="MenuItemIngredient",
        related_name="menu_items"
    )

    class Meta:
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["is_available"]),
        ]

    def __str__(self):
        return self.name


class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity_required = models.FloatField()

    class Meta:
        unique_together = ("menu_item", "ingredient")

    def __str__(self):
        return f"{self.menu_item.name} - {self.ingredient.name}"