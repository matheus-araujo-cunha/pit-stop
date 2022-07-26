from django.forms import model_to_dict
from rest_framework import serializers
from django.db import models
from carts.models import Cart

from orders.models import Order, OrderProducts
from products.models import Products
from products.serializers import ProductsSerializer
from users.serializers import UserSerializer


class OrderProductSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

class ProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ["stock","price","description"]

class OrderProdSerializer(serializers.ModelSerializer):
    product = ProdSerializer(many=False, read_only=True)
    class Meta:
        model = OrderProducts
        fields = "__all__"
class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    # products = OrderProdSerializer(many=True,read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id","date","user"]
