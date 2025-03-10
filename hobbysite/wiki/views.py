from django.views.generic import ListView, DetailView
from .models import Article

class WikiListView(ListView):
    model = Article
    template_name = "wikiList.html"
    context_object_name = "wikiList"

class WikiDetailView(DetailView):
    model = Article
    template_name = "wikiDetail.html"
    context_object_name = "wikiDetail"