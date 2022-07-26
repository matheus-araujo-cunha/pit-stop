from django.forms import model_to_dict
from rest_framework import serializers
from django.db import models
from carts.models import Cart

from orders.models import Order, OrderProducts
from products.models import Products
from products.serializers import ProductsSerializer


class OrderProductSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    products = ProductsSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ["id","date","products"]