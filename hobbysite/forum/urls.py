from django.urls import path
from .views import threadDetail, threadList


urlpatterns = [
    path('threads/', threadList, name='threadList'),
    path('thread/<int:thread_id>/', threadDetail, name='threadDetail'),
]


app_name = 'forum'