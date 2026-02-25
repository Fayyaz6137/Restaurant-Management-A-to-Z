from django.urls import path
from .views import PlaceOrderView, UserOrdersView

urlpatterns = [
    path("create/", PlaceOrderView.as_view(), name="place-order"),
    path("orders/", UserOrdersView.as_view(), name="user-orders"),
]
