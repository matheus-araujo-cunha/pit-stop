from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from carts.exceptions import NoProductsInStockError

from django.core.exceptions import ObjectDoesNotExist

from .serializers import (
    AddProductsInCartSerializer,
    RetrieveCartProductsSerializer,
)

from carts.models import Cart, CartProduct
from carts.permissions import IsOwnerCart
from carts.serializers import CartSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Products

from users.models import User


class RetrieveCreateDestroyAPIView(
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    generics.DestroyAPIView,
    generics.GenericAPIView,
):
    pass


class CartView(RetrieveCreateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        cart = Cart.objects.get(user=user)

        products = CartProduct.objects.filter(cart=cart)

        products = RetrieveCartProductsSerializer(products, many=True)

        serializer = self.get_serializer(cart)

        return Response({**serializer.data, "products": products.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except NoProductsInStockError:
            return Response(
                {"message": "No more products in stock"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except ObjectDoesNotExist:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        headers = self.get_success_headers(serializer.data)

        products = CartProduct.objects.filter(cart=serializer.data["id"])

        products = AddProductsInCartSerializer(products, many=True)

        return Response(
            {**serializer.data, "products": products.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        user: User = User.objects.get(email=self.request.user)
        list_uuid_products = serializer.validated_data["list_products"]

        return serializer.save(user=user, list_uuid=list_uuid_products)

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        cart = Cart.objects.get(user=user)

        cart_products = CartProduct.objects.filter(cart=cart)

        for product in cart_products:
            print(50 * "=", product)
            current_product = Products.objects.get(product_uuid=product.product_id)

            current_product.stock.quantity += product.amount
            current_product.stock.save()

        cart.products.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class CartDeleteProductView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerCart]

    lookup_field = "product_id"

    def destroy(self, request, *args, **kwargs):
        try:
            product = Products.objects.get(product_uuid=self.kwargs.get("product_id"))
            cart = Cart.objects.get(user=self.request.user)
            cart_product = CartProduct.objects.get(product=product)
        except ObjectDoesNotExist:
            return Response(
                {"message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        product.stock.quantity += 1
        product.stock.save()
        if cart_product.amount > 1:
            cart_product.amount -= 1
            cart_product.save()
        else:
            cart.products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
