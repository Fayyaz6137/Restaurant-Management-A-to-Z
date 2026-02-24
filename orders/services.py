from django.db import transaction
from decimal import Decimal
from .models import Order, OrderItem
from menu.models import MenuItem


@transaction.atomic
def place_order(user, branch, items_data):
    """
    items_data example:
    [
        {"menu_item_id": 1, "quantity": 2},
        {"menu_item_id": 3, "quantity": 1}
    ]
    """

    order = Order.objects.create(
        user=user,
        branch=branch,
        status="pending"
    )

    total_amount = Decimal("0.00")

    for item in items_data:
        menu_item = MenuItem.objects.select_for_update().get(
            id=item["menu_item_id"],
            is_available=True
        )

        quantity = item["quantity"]

        price = menu_item.price
        total_amount += price * quantity

        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=quantity,
            price_snapshot=price
        )

    order.total_amount = total_amount
    order.save()

    return order