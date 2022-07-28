from webbrowser import get
from django.shortcuts import render
from rest_framework import generics
from products.models import Products
from products.serializers import ProductsSerializer
from stock.models import Stock
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from products.permissions import IsAdmPermission


class ProductsView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmPermission]
    
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    def perform_create(self, serializer: ProductsSerializer):
        valid_stock = serializer.validated_data.get("stock")
        stock = Stock.objects.create(**valid_stock)
        serializer.save(stock=stock)
    


class ProductsViewId(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmPermission,IsAdminUser]

    queryset:Products.objects.all()
    serializer_class = ProductsSerializer