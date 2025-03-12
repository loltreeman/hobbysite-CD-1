from django.urls import path
from .views import commissions_list, commissions_detail

urlpatterns = [
    path('commissions/list', commissions_list, name ='commissions_list'),
    path('commissions/detail/<int:id>/', commissions_detail, name ='commissions_detail'),
]

app_name = "commissions" 