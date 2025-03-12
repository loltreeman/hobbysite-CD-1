from django.views.generic import ListView, DetailView
from django.http import HttpResponse 
from django.shortcuts import render
from .models import Article, ArticleCategory

# Create your views here 
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

def article_list(request):
    articles = Article.objects.all()
    ctx = {"articles_list": articles}
    return render(request, "article_list.html", ctx)

def article(request, pk):
    article = Article.objects.get(pk=pk)
    ctx = {
        "name": article.title,
        "category": article.category.name,
        "entry": article.entry,
        "created_on": article.created_on,
        "updated_on": article.updated_on,
    }
    return render(request, "article_detail.html", ctx)
