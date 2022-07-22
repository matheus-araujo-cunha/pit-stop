from django.urls import path
from products.views import ProductsView, ProductsViewId

urlpatterns = [
    path("products/",ProductsView.as_view()),
    path("products/<int:pk>",ProductsViewId.as_view())
]