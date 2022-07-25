from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import RetrieveProductsSerialize

from carts.models import Cart, CartProduct
from carts.permissions import IsOwnerCart
from carts.serializers import CartSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Products

from users.models import User


class CreateDestroyAPIView(
    generics.CreateAPIView,
    generics.DestroyAPIView,
    generics.GenericAPIView,
):
    pass


class CartView(CreateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        products = CartProduct.objects.filter(cart=serializer.data["id"])

        products = RetrieveProductsSerialize(products, many=True)

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

        cart.products.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class RetrieveCartProductsView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        cart = Cart.objects.get(user=user)

        products = CartProduct.objects.filter(cart=cart)

        products_serialized = RetrieveProductsSerialize(products, many=True)
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return Response({**serializer.data, "products": products_serialized.data})


class CartDeleteProductView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerCart]

    lookup_field = "product_id"

    def destroy(self, request, *args, **kwargs):
        product = Products.objects.get(product_uuid=self.kwargs.get("product_id"))

        cart = Cart.objects.get(user=self.request.user)

        cart_product = CartProduct.objects.get(product=product)

        if cart_product.amount > 1:
            cart_product.amount -= 1
            cart_product.save()
        else:
            cart.products.remove(product)

        return Response(status=status.HTTP_204_NO_CONTENT)
