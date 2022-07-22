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
        order = Order.objects.create(user=user)
        try:
            cart = Cart.objects.get(user=user)
            for product in cart.products:
                new_product = Products.objects.get(product_uuid=product)
                OrderProducts.objects.create(order = order,product = new_product,value = new_product.price)
            print(OrderProducts.objects.filter(order=order))
            cart.products.clear()
        except:
            print("error")
        serializer.save(user=user)

class RetrieveOrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
