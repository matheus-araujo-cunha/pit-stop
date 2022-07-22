from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


from carts.models import Cart
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

    def perform_create(self, serializer):
        user: User = User.objects.get(email=self.request.user)
        list_uuid_products = serializer.validated_data["list_products"]

        return serializer.save(user=user, list_uuid=list_uuid_products)

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        cart = Cart.objects.get(user=user)
        print("CARRINHO", cart)

        cart.products.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # instance.clear()


class RetrieveCartProductsView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class CartDeleteProductView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerCart]

    lookup_field = "product_id"

    def destroy(self, request, *args, **kwargs):
        product = Products.objects.get(product_uuid=self.kwargs.get("product_id"))

        cart = Cart.objects.get(user=self.request.user)

        cart.products.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
