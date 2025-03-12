from django.contrib import admin
from .models import ProductType, Product



class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType

    list_display = ['name']
    list_filter = ['name']


class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ['name']
    list_filter = ['name']

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)