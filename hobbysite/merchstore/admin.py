from django.contrib import admin
from .models import ProductType, Product


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price')
    search_fields = ('name', 'product_type__name', 'description')
    list_filter = ('product_type',)
    ordering = ['name']


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)