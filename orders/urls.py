from django.urls import path

from orders.views import RetrieveOrderView, ListOrdersView

urlpatterns = [
    path("order/", ListOrdersView.as_view()),
    path("order/<int:pk>", RetrieveOrderView.as_view())
]
