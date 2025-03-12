from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()

