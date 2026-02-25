import os

from celery import shared_task
from django.core.mail import send_mail
from django.db import models
from .models import BranchInventory
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_low_stock_alert():
    low_stock_ingredients = BranchInventory.objects.filter(stock_quantity__lte=models.F('low_stock_threshold'))
    for bi in low_stock_ingredients:
        # send_mail(
        #     subject=f"Low Stock Alert: {bi.ingredient.name}",
        #     message=f"Ingredient {bi.ingredient.name} is low in stock: {bi.stock_quantity}left.",
        #     from_email="fizhassolsamor@gmail.com",
        #     recipient_list=["fayyazhs107@gmail.com"],
        # )

        # Mail Object Setup
        email = EmailMessage()
        email['from'] = 'Fayyaz Shah'
        email['to'] = 'fayyazhs107@gmail.com'
        email['subject'] = f"Low Stock Alert: {bi.ingredient.name}"
        email.set_content = f"Ingredient {bi.ingredient.name} is low in stock: {bi.stock_quantity}left."

        # Sending Mail
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=str(os.getenv('EMAIL_HOST_USER')), password=str(os.getenv('EMAIL_HOST_PASSWORD')))
            connection.send_message(email)

