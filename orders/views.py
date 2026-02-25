from django.shortcuts import render
from rest_framework import generics, status
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from menu.models import Category, MenuItem
from menu.serializers import CategorySerializer
from .models import Order
from .serializers import OrderSerializer
from .services import place_order
from rest_framework.permissions import IsAuthenticated, AllowAny
from restaurants.models import Branch



# Create order endpoint
class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        branch_id = request.data.get("branch_id")
        items_data = request.data.get("items")

        if not branch_id or not items_data:
            return Response(
                {"error": "branch_id and items are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the Branch instance
        try:
            branch = Branch.objects.get(id=branch_id, is_active=True)
        except Branch.DoesNotExist:
            return Response(
                {"error": "Branch does not exist or is inactive"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = place_order(user, branch, items_data)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "One of the menu items does not exist or is unavailable"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {f"{e} error": "Order could not be processed"},
                status=status.HTTP_400_BAD_REQUEST
            )


# List user orders
class UserOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .select_related("branch")
            .prefetch_related("items__menu_item")
        )
