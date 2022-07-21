from django.urls import path
from .views import CartView, CartUpdateProductView

urlpatterns = [
    path("carts/", CartView.as_view()),
    path("carts/products/<int:product_id>/", CartUpdateProductView.as_view()),
]
