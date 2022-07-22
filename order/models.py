from django.db import models
from django.utils import timezone

class Order(models.Model):
    date = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="order")

class OrderProducts(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)    
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey("products.Products", on_delete=models.CASCADE, related_name="order_products")

