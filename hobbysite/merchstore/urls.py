from django.contrib import admin
from django.urls import path 
from .views import merchList, merchDetail



urlpatterns = [
    path('merchstore/items', merchList, name='merchlist'),
    path('merchstore/item/<int:pk>', merchDetail, name='merchdetail')
]

app_name = "merchstore"