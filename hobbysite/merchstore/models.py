from django.db import models


class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType,null=True ,on_delete=models.SET_NULL, related_name='products')
    owner = models.ForeignKey('user_management.Profile',on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('on_sale', 'On Sale'),
        ('out_of_stock', 'Out of Stock'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    buyer = models.ForeignKey('user_management.Profile', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    STATUS_CHOICES = (
        ('on_cart', 'On Cart'),
        ('to_pay', 'To Pay'),
        ('to_ship', 'To Ship'),
        ('to_receive', 'To Recieve'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(max_length=20, choices = STATUS_CHOICES)
    createdOn = models.DateTimeField(auto_now_add=True)