from rest_framework import serializers
from carts.exceptions import NoProductsInStockError
from products.models import Products

from django.core.exceptions import ObjectDoesNotExist


from .models import Cart, CartProduct
from users.serializers import UserSerializer


class ProductCartSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()


class AddProductsInCartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CartProduct
        exclude = ["cart"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ["stock", "description", "warranty", "price"]


class RetrieveCartProductsSerializer(serializers.ModelSerializer):
    item = ProductSerializer(read_only=True, source="product")

    class Meta:
        model = CartProduct
        exclude = ["cart", "product"]


class CartSerializer(serializers.ModelSerializer):
    list_products = ProductCartSerializer(
        many=True,
        write_only=True,
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "list_products",
        ]
        read_only_fields = [
            "user",
        ]

    def create(self, validated_data: dict):
        cart_user, _ = Cart.objects.get_or_create(user=validated_data["user"])

        for product in validated_data["list_uuid"]:
            new_product: Products = Products.objects.get(
                product_uuid=product["product_uuid"]
            )

            quantity_in_stock = new_product.stock.quantity

            if quantity_in_stock <= 1:
                raise NoProductsInStockError()

            new_product.stock.quantity -= 1
            new_product.stock.save()
            try:
                product_cart: CartProduct = CartProduct.objects.get(
                    product_id=new_product.product_uuid
                )

                product_cart.amount += product["amount"]
                product_cart.save()
                continue

            except ObjectDoesNotExist:
                mapped_product = {
                    "price": new_product.price,
                    "amount": 1,
                    "cart": cart_user,
                    "product": new_product,
                }

                CartProduct.objects.create(**mapped_product)

        return cart_user
