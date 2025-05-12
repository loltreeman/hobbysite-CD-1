from django.urls import path
from .views import  ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'
urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('article/add/', ArticleCreateView.as_view(), name='article_add'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)