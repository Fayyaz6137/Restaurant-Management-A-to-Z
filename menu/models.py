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
    stock_quantity = models.FloatField(default=0)  # track available quantity
    unit = models.CharField(max_length=20, default="pcs")  # kg, pcs, liters etc.
    low_stock_threshold = models.FloatField(default=10)  # alert if below this

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold


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
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='menuitemingredient_set')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.FloatField()

    class Meta:
        unique_together = ("menu_item", "ingredient")

    def __str__(self):
        return f"{self.menu_item.name} → {self.ingredient.name} ({self.quantity_required})"

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_ordered = models.FloatField()
    received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ingredient.name} → {self.quantity_ordered} from {self.supplier.name}"