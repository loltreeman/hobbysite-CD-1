from django.urls import path
from .views import threadDetail, threadList

app_name = 'forum'

urlpatterns = [
    path('threads/', threadList, name='threadList'),
    path('thread/<int:threadId>/', threadDetail, name='threadDetail'),
]