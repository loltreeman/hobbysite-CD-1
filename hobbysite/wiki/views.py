from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "wiki/articles_list.html"
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "wiki/article_detail.html"
    context_object_name = "article"