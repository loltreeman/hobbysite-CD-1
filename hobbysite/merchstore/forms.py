from django import forms
from .models import ProductType, Product, Transaction

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = '__all__'
        exclude = ['owner']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']


