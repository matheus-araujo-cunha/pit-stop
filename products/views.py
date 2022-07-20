from django.shortcuts import render
from rest_framework import generics

from products.models import Products
from products.serializers import ProductsSerializer



class ProductsView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


    def perform_create(self, serializer: ProductsSerializer):
        valid_stock = serializer.validated_data.get("stock")
        stock = Stock.objects.create(**valid_stock)

        serializer.save(stock=stock)