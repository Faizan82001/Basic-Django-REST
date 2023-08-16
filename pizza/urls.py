from django.urls import path, include
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("pizzas",PizzaList.as_view(), name='pizza-list'),
    path("pizzas/<uuid:pk>", PizzaDetail.as_view(), name='pizza-detail'),
    path("orders", OrderList.as_view(), name='orders'),
    path("orders/<uuid:pk>", OrderDetail.as_view(), name='order-detail'),
]