from dataclasses import fields
from rest_framework import serializers
from products.models import Products
from stock.serializers import StockSerializer


class ProductsSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        depth = 1
        model = Products
        fields = (
            "product_uuid",
            "name",
            "description",
            "manufacturer",
            "warranty",
            "price",
            "categorie",
            "stock",
        )
