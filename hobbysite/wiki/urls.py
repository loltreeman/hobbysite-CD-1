from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("article/add/", views.ArticleCreateView.as_view(), name="article_create"),
    path("article/<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="article_update"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "wiki"