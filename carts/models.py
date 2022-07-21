from django.db import models


class Cart(models.Model):

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="cart"
    )

    products = models.ManyToManyField(
        "products.Product", on_delete=models.CASCADE, related_name="carts", null=True
    )
