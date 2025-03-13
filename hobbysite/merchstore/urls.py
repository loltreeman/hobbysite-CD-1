from django.urls import path
from .views import merchList, merchDetail


urlpatterns = [
    path('items/', merchList, name='merch_list'),
    path('item/<int:pk>/', merchDetail, name='merch_detail'),
]


app_name = 'merchstore'