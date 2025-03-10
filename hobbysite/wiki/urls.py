from django.urls import path
from .views import WikiListView, WikiDetailView

urlpatterns = [
    path('/wiki/articles', WikiListView.as_view(), name="wikiList"),
    path('/wiki/article/<int:pk>', WikiDetailView.as_view(), name="wikiDetail"),
]

app_name = 'wiki'