from django.contrib import admin
from .models import Branch, Restaurant, BranchInventory, Staff

admin.site.register(Restaurant)
admin.site.register(Branch)
admin.site.register(BranchInventory)
admin.site.register(Staff)