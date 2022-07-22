from django.urls import path
from .views import CartView, CartDeleteProductView, RetrieveCartProductsView

urlpatterns = [
    path("carts/", CartView.as_view()),
    path("carts/products/<str:product_id>/", CartDeleteProductView.as_view()),
    path("carts/<int:id>/", RetrieveCartProductsView.as_view()),
]
