from django.urls import path
from .views import MenuListView, PlaceOrderView, UserOrdersView

urlpatterns = [
    path("menu/", MenuListView.as_view(), name="menu-list"),
    path("order/create/", PlaceOrderView.as_view(), name="place-order"),
    path("orders/", UserOrdersView.as_view(), name="user-orders"),
]