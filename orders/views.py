from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from menu.models import Category, MenuItem
from menu.serializers import CategorySerializer
from .models import Order
from .serializers import OrderSerializer
from .services import place_order
from rest_framework.permissions import IsAuthenticated, AllowAny


# List all menu categories with items
class MenuListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related("items__menuitemingredient_set__ingredient").all()
    serializer_class = CategorySerializer


# Create order endpoint
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        branch_id = request.data.get("branch_id")
        items_data = request.data.get("items")  # list of {"menu_item_id": X, "quantity": Y}

        if not branch_id or not items_data:
            return Response({"error": "branch_id and items are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = place_order(user, branch_id, items_data)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# List user orders
class UserOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__menu_item")
