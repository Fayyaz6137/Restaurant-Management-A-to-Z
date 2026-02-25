from django.db import transaction
from decimal import Decimal
from .models import Order, OrderItem
from menu.models import MenuItem, MenuItemIngredient


@transaction.atomic
def place_order(user, branch, items_data):
    """
    items_data example:
    [
        {"menu_item_id": 1, "quantity": 2},
        {"menu_item_id": 3, "quantity": 1}
    ]
    """

    order = Order.objects.create(user=user, branch=branch, status="pending")

    for item_data in items_data:
        menu_item_id = item_data['menu_item_id']
        quantity = item_data['quantity']

        menu_item = MenuItem.objects.select_for_update().get(id=menu_item_id)

        # check stock for all ingredients
        ingredients = MenuItemIngredient.objects.filter(menu_item=menu_item).select_for_update()
        for mi in ingredients:
            required = mi.quantity_required * quantity
            if mi.ingredient.stock_quantity < required:
                raise ValueError(f"Insufficient stock for {mi.ingredient.name}")

        # Deduct ingredients
        for mi in ingredients:
            mi.ingredient.stock_quantity -= mi.quantity_required * quantity
            mi.ingredient.save()

        # Create OrderItem
        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity,
            price_snapshot=menu_item.price
        )

    # calculate total
    total = sum([oi.menu_item.price * oi.quantity for oi in order.items.all()])
    order.total_amount = total
    order.save()

    return order
