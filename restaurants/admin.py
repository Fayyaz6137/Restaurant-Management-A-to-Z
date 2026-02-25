from django.contrib import admin
from .models import Branch, Restaurant

admin.site.register(Restaurant)
admin.site.register(Branch)