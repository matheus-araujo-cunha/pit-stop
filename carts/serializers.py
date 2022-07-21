from rest_framework import serializers
from products.models import Products

from products.serializers import ProductsSerializer
from .models import Cart


class ProductCartSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()


class CartSerializer(serializers.ModelSerializer):
    products = ProductCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "products", "user"]
        read_only_fields = ["user"]

    def create(self, validate_data: dict):
        user = validate_data.pop("user")
        cart: Cart = Cart.objects.create(user=user)
        print(50 * "=", "TO NO CREATEEEE", 50 * "=")

        for product in validate_data["products"]:
            cart.products.add(product)
        return cart
