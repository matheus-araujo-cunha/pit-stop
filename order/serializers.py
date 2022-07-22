from rest_framework import serializers
from django.db import models

from order.models import Order


class OrderProductSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ["id","date"]
        # read_only_fields = ["users"]
