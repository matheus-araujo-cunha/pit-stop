from django.db import models


class Cart(models.Model):

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="cart"
    )

    products = models.ManyToManyField(
        "products.Products", related_name="carts", through="CartProduct"
    )


class CartProduct(models.Model):
    product = models.ForeignKey("products.Products", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=1)
