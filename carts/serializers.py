from rest_framework import serializers
from products.models import Products

from products.serializers import ProductsSerializer
from .models import Cart


class ProductCartSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()


class CartSerializer(serializers.ModelSerializer):
    list_products = ProductCartSerializer(
        many=True,
        write_only=True,
    )
    cart_products = ProductsSerializer(read_only=True, many=True, source="products")

    class Meta:
        model = Cart
        fields = ["id", "cart_products", "user", "list_products"]
        read_only_fields = ["user"]

    def create(self, validated_data: dict):
        cart_user: Cart = Cart.objects.get(user=validated_data["user"])

        for product in validated_data["list_uuid"]:
            new_product = Products.objects.get(product_uuid=product["product_uuid"])
            cart_user.products.add(new_product)
        return cart_user


