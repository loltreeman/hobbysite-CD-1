from django.urls import path
from .views import commissions_list, commissions_detail

urlpatterns = [
    path('list/', commissions_list, name ='commissions_list'),
    path('detail/<int:id>/', commissions_detail, name ='commissions_detail'),
]

app_name = "commissions" 