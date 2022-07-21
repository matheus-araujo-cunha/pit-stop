from django.db import models

class Stock(models.Model):
    quantity = models.FloatField(default=1)
    categorie = models.CharField(max_length=50, unique=True)
