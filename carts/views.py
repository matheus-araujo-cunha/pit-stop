from xml.dom import NotFoundErr
from rest_framework import generics

from carts.models import Cart
from carts.serializers import CartSerializer
from rest_framework.authentication import TokenAuthentication

from users.models import User


class CreateUpdateDestroyAPIView(
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
    generics.GenericAPIView,
):
    pass


class CartView(CreateUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user: User = User.objects.get(self.request.user)

        if not user.cart:
            Cart.objects.create(user=user)

        products = serializer.products

        for product in products:
            new_product = Products.objects.get(name=product)
            if not new_product:
                raise NotFoundErr()
            user.cart.add(new_product)
