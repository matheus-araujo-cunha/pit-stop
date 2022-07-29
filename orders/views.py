from datetime import datetime
from django.shortcuts import render
from rest_framework import  generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import  RetrieveAPIView,ListCreateAPIView
from carts.models import Cart, CartProduct
from products.models import Products
from rest_framework import status
from rest_framework.response import Response

from users.models import User
from .models import Order, OrderProducts
from .serializers import OrderProdSerializer, OrderSerializer


class ListOrdersView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        products = OrderProducts.objects.filter(order_id=serializer.data["id"])
        products_serialized = OrderProdSerializer(products, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response({**serializer.data,"products":products_serialized.data}, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        user: User = User.objects.get(email=self.request.user)
        order = serializer.save(user=user)
        cart = Cart.objects.get(user=user)
        cart_products = CartProduct.objects.filter(cart=cart)
        for product in cart_products.all():
            OrderProducts.objects.create(order = order,product_id = product.product_id,value = product.price,amount=product.amount)
        cart.products.clear()

class RetrieveOrderView(RetrieveAPIView):
    queryset = OrderProducts.objects.all()
    serializer_class = OrderProdSerializer
