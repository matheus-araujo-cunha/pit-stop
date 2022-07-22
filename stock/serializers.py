from rest_framework import serializers

class StockSerializer(serializers.Serializer):
    quantity = serializers.FloatField(default=1)
    categorie = serializers.CharField(max_length=50)
    