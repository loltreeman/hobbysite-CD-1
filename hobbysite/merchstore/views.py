from django.shortcuts import render
from .models import Product, ProductType


def merchList(request):
    merchType = Product.objects.all().order_by('name')
    ctx = {"merchType": merchType}
    return render(request, "merchlist.html", ctx)

def merchDetail(request,pk):
    merch = Product.objects.get(pk=pk)
    ctx = {"merch":merch}
    return render(request,"merchdetail.html", ctx)

