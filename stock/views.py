from django.shortcuts import render
from stock.models import Stock
from rest_framework.views import APIView, Request, Response, status

from stock.serializers import StockSerializer

class StockView(APIView):
    def get(self, request: Request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(instance=stocks, many=True)

        return Response({'stocks': serializer.data}, status.HTTP_200_OK)
