from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=255)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()

    class Meta:
        ordering = ['name']

