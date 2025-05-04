from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Article, Comment
from user_management.models import Profile  # import Profile from user_management
from .forms import CommentForm

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'all_articles'  # we’ll still pass this if needed

    def get_queryset(self):
        # return all articles except those by this user
        return Article.objects.exclude(author=self.request.user.profile).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The ones you created:
        context['user_articles'] = Article.objects.filter(author=self.request.user.profile)
        # Group the “others” (which come from get_queryset())
        grouped = {}
        for a in context['all_articles']:
            grouped.setdefault(a.category, []).append(a)
        context['grouped_articles'] = grouped.items()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        context['related_articles'] = Article.objects.filter(
            author=article.author
        ).exclude(pk=article.pk)[:2]
        context['images'] = article.images.all()
        context['comments'] = Comment.objects.filter(article=article).order_by('-created_on')
        context['comment_form'] = CommentForm()
        if self.request.user.profile == article.author:
            context['edit_link'] = True

        context['previous_article'] = Article.objects.filter(
            created_on__lt=article.created_on
        ).order_by('-created_on').first()
        context['next_article'] = Article.objects.filter(
            created_on__gt=article.created_on
        ).order_by('created_on').first()
        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = Profile.objects.get(user=request.user)
            comment.article = article
            comment.save()
        return redirect('blog:article_detail', pk=article.pk)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'article_add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article_list')

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'article_edit.html'

    def test_func(self):
        return self.request.user.profile == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})