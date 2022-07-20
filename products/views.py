from django.shortcuts import render
from rest_framework import generics

from products.models import Products
from products.serializers import ProductsSerializer



class ProductsView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

