from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Transaction
from .forms import ProductForm, ProductTypeForm, TransactionForm


def merchList(request):
    merch_types = Product.objects.all()
    ctx = {"merch_types": merch_types}
    return render(request, "merch_list.html", ctx)


def merchDetail(request, pk):
    merch = get_object_or_404(Product, pk=pk)
    can_purchase = True
    if request.method == 'POST':
        transactForm = TransactionForm(request.POST)
        if transactForm.is_valid():
            transaction = transactForm.save(commit=False)
            transaction.product = merch
            transaction.buyer = request.user.profile
            transaction.status = 'on_cart'

            merch.stock -= transaction.amount
            if merch.stock == 0:
                 merch.status = 'out_of_stock'
                 can_purchase = False
            merch.save()
            transaction.save()
            redirect('merchstore:merch_cart')
    else:
            transactForm = TransactionForm(request.POST)
    ctx = {"merch": merch , "transact_form" : transactForm, "can_purchase":can_purchase}
    return render(request, "merch_detail.html", ctx)

def merchCreate(request):
    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        productTypeform = ProductTypeForm(request.POST)
        if productform.is_valid():
            productform.save()
        elif productTypeform.is_valid():
            productTypeform.save()
    else:
        productform = ProductForm(request.POST, request.FILES)
        productTypeform = ProductTypeForm(request.POST)
        products = Product.objects.all()

        ctx = {"products": products}

        print(f"request type: {request.method}")
        print(f"ctx: {ctx}")

    return render(request,'merch_create.html',{"product_form": productform, "productType_form":productTypeform})

def merchUpdate(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        updateform = ProductForm(request.POST, instance=instance)
        if updateform.is_valid():
            updateform.save()
    else:
             updateform = ProductForm(instance=instance)
    return render(request, 'merch_update.html', {'update_form':updateform})

def merchCart(request):
    transaction = Transaction.objects.filter(buyer=request.user.profile, status='On Cart').select_related('product')
    ctx = {"transactions": transaction}
    return render(request, "merch_cart.html", ctx)

def merchTransactions(request):
    transaction = Transaction.objects.filter(product__owner=request.user.profile).select_related('buyer', 'product')
    ctx = {'transactions': transaction}
    return render(request, 'merch_transaction.html', ctx)