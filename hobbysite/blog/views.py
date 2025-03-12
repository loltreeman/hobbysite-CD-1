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

