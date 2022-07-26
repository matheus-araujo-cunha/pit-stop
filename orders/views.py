from datetime import datetime
from django.shortcuts import render
from rest_framework import  generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import  RetrieveAPIView,ListCreateAPIView
from carts.models import Cart
from products.models import Products

from users.models import User
from .models import Order, OrderProducts
from .serializers import OrderSerializer


class ListOrdersView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def perform_create(self, serializer):
        user: User = User.objects.get(email=self.request.user)
        order = serializer.save(user=user)
        cart = Cart.objects.get(user=user)
        for product in cart.products.all():
            OrderProducts.objects.create(order = order,product = product,value = product.price)
        cart.products.clear()

class RetrieveOrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
