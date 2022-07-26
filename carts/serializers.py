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

                product_cart.amount += 1
                product_cart.save()
                continue

            except ObjectDoesNotExist:
                mapped_product = {
                    "price": new_product.price,
                    "amount": 1,
                    "cart": cart_user,
                    "product": new_product,
                }


