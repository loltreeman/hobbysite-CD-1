from django.urls import path
from .views import ThreadListView, ThreadDetailView, ThreadCreateView, ThreadUpdateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'forum'

urlpatterns = [
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/add/', ThreadCreateView.as_view(), name='thread_create'),
    path('thread/<int:pk>/edit/', ThreadUpdateView.as_view(), name='thread_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)