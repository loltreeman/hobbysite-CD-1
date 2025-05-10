from django.contrib import admin
from .models import ProductType, Product, Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price')
    search_fields = ('name', 'product_type__name', 'owner','description','price','stock','status')
    list_filter = ('product_type',)
    ordering = ['name']

class TransactionAdmin(admin.ModelAdmin):
    list_dispay = ('buyer','product','amount','status')

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)