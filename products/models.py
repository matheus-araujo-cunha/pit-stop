from uuid import uuid4
from django.db import models


class Products(models.Model):

    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=50)
    warranty = models.IntegerField()
    img = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50)

    stock = models.OneToOneField(
        "stock.Stock", on_delete=models.CASCADE, related_name="product"
    )
