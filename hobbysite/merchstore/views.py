from django.shortcuts import render, get_object_or_404
from .models import Product


def merchList(request):
    merch_types = Product.objects.all()
    ctx = {"merch_types": merch_types}
    return render(request, "merch_list.html", ctx)


def merchDetail(request, pk):
    merch = get_object_or_404(Product, pk=pk)
    ctx = {"merch": merch}
    return render(request, "merch_detail.html", ctx)