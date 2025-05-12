from django.urls import path
from .views import commissions_list, commissions_detail, create_view, update_view, apply_to_job, create_job, job_view

urlpatterns = [
    path('list/', commissions_list, name ='commissions_list'),
    path('detail/<int:id>/', commissions_detail, name ='commissions_detail'),
    path('add/', create_view, name ='create_commissions'),
    path('<int:id>/edit/', update_view, name ='update_commissions'),
    path('job/<int:job_id>/apply/', apply_to_job, name='apply_to_job'),
    path('detail/<int:commission_id>/addjob', create_job, name='create_job'),
    path('job/<int:job_id>/', job_view, name='job_view')

]

app_name = "commissions" 