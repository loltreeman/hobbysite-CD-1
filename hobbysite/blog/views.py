from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Article, Comment, ArticleCategory
from user_management.models import Profile 
from .forms import ArticleForm, CommentForm

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'all_articles' 

    def get_queryset(self):
        return Article.objects.exclude(author=self.request.user.profile).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_articles'] = Article.objects.filter(author=self.request.user.profile)
        grouped = {}
        for a in context['all_articles']:
            grouped.setdefault(a.category, []).append(a)
        context['grouped_articles'] = grouped.items()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        context['related_articles'] = Article.objects.filter(author=article.author).exclude(pk=article.pk)[:2]
        context['images'] = article.images.all()
        context['comments'] = Comment.objects.filter(article=article).order_by('-created_on')
        context['comment_form'] = CommentForm()
        if self.request.user.profile == article.author:
            context['edit_link'] = True

        context['previous_article'] = Article.objects.filter(created_on__lt=article.created_on).order_by('-created_on').first()
        context['next_article'] = Article.objects.filter(created_on__gt=article.created_on).order_by('created_on').first()
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
    form_class = ArticleForm
    template_name = 'blog/article_add.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = ArticleCategory.objects.all()
        return form

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()

        new_category_name = post_data.get('new_category')
        if new_category_name:
            category, created = ArticleCategory.objects.get_or_create(name=new_category_name.strip())
            post_data['category'] = category.id  

        self.request.POST = post_data 

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article_list')

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'blog/article_edit.html'

    def test_func(self):
        return self.request.user.profile == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})
