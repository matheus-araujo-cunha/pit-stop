from django.urls import path

from stock.views import StockView

urlpatterns = [
    path("stock/", StockView.as_view())
]
