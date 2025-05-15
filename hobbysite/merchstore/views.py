from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Transaction
from .forms import ProductForm, ProductTypeForm, TransactionForm
from django.contrib.auth.decorators import login_required


def merchList(request):
    user_profile = getattr(request.user, "profile", None)
    
    if request.user.is_authenticated:
         user_products = Product.objects.filter(owner=user_profile)
         other_products = Product.objects.exclude(owner=user_profile)

    else:
         user_products = None
         other_products = Product.objects.all()
    ctx = {"user_products": user_products, "other_products":other_products}
    return render(request, "merchstore/merch_list.html", ctx)

@login_required
def merchDetail(request, pk):
    merch = get_object_or_404(Product, pk=pk)
    can_purchase = (merch.owner != request.user.profile) and merch.stock > 0

    if request.method == 'POST':
        transact_form = TransactionForm(request.POST)
        if transact_form.is_valid():
            amount = transact_form.cleaned_data['amount']

            if amount > merch.stock:
                transact_form.add_error(
                    'amount',
                    f'You can only buy {merch.stock} item{"s" if merch.stock != 1 else ""} or less.'
                )
            else:
                transaction = transact_form.save(commit=False)
                transaction.product = merch
                transaction.buyer = request.user.profile
                transaction.status = 'on_cart'

                merch.stock -= amount
                if merch.stock == 0:
                    merch.status = 'out_of_stock'
                    can_purchase = False
                merch.save()
                transaction.save()
                return redirect('merchstore:merch_cart')
    else:
        transact_form = TransactionForm()

    return render(request, 'merchstore/merch_detail.html', {
        'merch': merch,
        'transact_form': transact_form,
        'can_purchase': can_purchase,
    })

@login_required
def merchCreate(request):
    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        productTypeform = ProductTypeForm(request.POST)
        if productform.is_valid():
            product = productform.save(commit=False)
            product.owner = request.user.profile
            productform.save()
        elif productTypeform.is_valid():
            productTypeform.save()
    else:
        productform = ProductForm(request.POST, request.FILES)
        productTypeform = ProductTypeForm(request.POST)

    return render(request,'merchstore/merch_create.html',{"product_form": productform, "productType_form":productTypeform})

@login_required
def merchUpdate(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        updateform = ProductForm(request.POST, instance=instance)
        if updateform.is_valid():
            updateform.save()
            return redirect('merchstore:merch_list')
    else:
             updateform = ProductForm(instance=instance)
    return render(request, 'merchstore/merch_update.html', {'update_form':updateform})

@login_required
def merchCart(request):
    transaction = Transaction.objects.filter(buyer=request.user.profile, status='on_cart').select_related('product')
    ctx = {"transactions": transaction}
    return render(request, "merchstore/merch_cart.html", ctx)

@login_required
def merchTransactions(request):
    transaction = Transaction.objects.filter(product__owner=request.user.profile).select_related('buyer', 'product').order_by('buyer')
    ctx = {'transactions': transaction}
    return render(request, 'merchstore/merch_transaction.html', ctx)