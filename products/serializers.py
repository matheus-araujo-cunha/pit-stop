from rest_framework import serializers
from products.models import Products
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Products
        fields =(
        "product_uuid",
        "name",
        "description",
        "manufacturer",
        "warrant",
        "price",
        "stock",
        "orders",
    )
        