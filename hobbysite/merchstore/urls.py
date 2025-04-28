from django.urls import path
from .views import merchList, merchDetail, merchCreate, merchUpdate, merchCart, merchTransactions


urlpatterns = [
    path('items/', merchList, name='merch_list'),
    path('item/<int:pk>/', merchDetail, name='merch_detail'),
    path('item/add', merchCreate, name='merch_create'),
    path('item/<int:pk>/edit', merchUpdate, name = 'merch_update'),
    path('cart/', merchCart, name='merch_cart'),
    path('transactions/', merchTransactions, name ='merch_transactions'),
]


app_name = 'merchstore'