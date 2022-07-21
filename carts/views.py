from xml.dom import NotFoundErr
from rest_framework import generics

from carts.models import Cart
from carts.permissions import IsOwnerCart
from carts.serializers import CartSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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

    def perform_create(self, serializer):
        user: User = User.objects.get(self.request.user)
        products = serializer.validated_data["products"]

        cart_user = Cart.objects.get(user=user)

        if not cart_user:
            return serializer.save(user=user, products=products)

        for product in products:
            new_product = Products.objects.get(name=product)
            if not new_product:
                raise NotFoundErr()
            cart_user.add(new_product)

        return cart_user

        # for product in products:
        #     new_product = Products.objects.get(name=product)
        #     if not new_product:
        #         raise NotFoundErr()
        #     user.cart.add(new_product)

    def perform_destroy(self, instance):
        instance.clear()


class CartUpdateProductView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerCart]

    lookup_field = "product_id"

    def destroy(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs.get("product_id"))

        cart = Cart.objects.get(user=self.request.user)

        cart.products.remove(product)
