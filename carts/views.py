from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist

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

        print("\n\n", user, "\n\n")

        list_uuid_products = serializer.validated_data["products"]
        try:
            cart_user: Cart = Cart.objects.get(user=user)
            print("PRODUTOSSSSS", cart_user.products)
            for product in list_uuid_products:
                new_product = Products.objects.get(product_uuid=product)
                cart_user.products.add(new_product)

            print(50 * "=", cart_user, 50 * "=")

            return cart_user
        except ObjectDoesNotExist:

            products = []
            for product in list_uuid_products:
                products.append(
                    Products.objects.get(product_uuid=product["product_uuid"])
                )
            serializer.save(user=user, products=products)
            cart_user = Cart.objects.get(user=user)
            return

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
