from celery import shared_task
from django.core.mail import send_mail
from django.db import models

from .models import Ingredient


@shared_task
def send_low_stock_alert():
    low_stock_ingredients = Ingredient.objects.filter(stock_quantity__lte=models.F('low_stock_threshold'))
    for ing in low_stock_ingredients:
        send_mail(
            subject=f"Low Stock Alert: {ing.name}",
            message=f"Ingredient {ing.name} is low in stock: {ing.stock_quantity}{ing.unit} left.",
            from_email="fizhassolsamor@gmail.com",
            recipient_list=["fayyazhs107@gmail.com"],
        )
