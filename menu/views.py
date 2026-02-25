from rest_framework import generics
from django.core.cache import cache
from menu.models import Category
from menu.serializers import CategorySerializer
from rest_framework.permissions import AllowAny


# List all menu categories with items
class MenuListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        cached = cache.get("menu_cache")
        if cached:
            return cached

        queryset = Category.objects.prefetch_related("items__menuitemingredient_set__ingredient").all()
        cache.set("menu_cache", queryset, timeout=60 * 60)  # cache for 1 hour
        return queryset


from django.shortcuts import render

# Create your views here.
