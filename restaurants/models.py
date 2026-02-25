from django.contrib.auth import get_user_model
from django.db import models

from menu.models import Ingredient

User = get_user_model()
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100,default='A Branch')
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    city = models.CharField(max_length=100)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.city}"


class BranchInventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="inventory")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    stock_quantity = models.FloatField(default=0)
    low_stock_threshold = models.FloatField(default=10)  # alert if below this

    class Meta:
        unique_together = ("branch", "ingredient")

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold

    def __str__(self):
        return f"{self.branch.name} → {self.ingredient.name}: {self.stock_quantity}"


class Staff(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="staff")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=(("chef", "Chef"), ("waiter", "Waiter"), ("manager", "Manager")))

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.branch.name}"