from django.urls import path

from order.views import RetrieveOrderView, ListOrdersView

urlpatterns = [
    path("order/", ListOrdersView.as_view())
    # path("order/<>")
]
