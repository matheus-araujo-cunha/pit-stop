from django.db import models

class Stock(models.Model):
    quantity = models.FloatField(default=1)