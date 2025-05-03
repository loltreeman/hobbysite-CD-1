from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy  # Use reverse_lazy for redirect URL
from .models import Article, ArticleCategory, Comment, ArticleImage, Profile  # Ensure Profile is imported
from .forms import CommentForm

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'all_articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # User's articles
        context['user_articles'] = Article.objects.filter(author=self.request.user.profile)

        # Group articles by category
        grouped = {}
        for article in Article.objects.select_related('category'):
            grouped.setdefault(article.category, []).append(article)
        
        # Exclude articles created by the logged-in user from the "All Articles" group
        context['grouped_articles'] = grouped.items()

        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        # Get related articles by the same author
        context['related_articles'] = Article.objects.filter(author=article.author).exclude(pk=article.pk)

        # Image gallery (if you have images related to the article)
        context['images'] = ArticleImage.objects.filter(article=article)

        # Comments, sorted by creation date (most recent first)
        context['comments'] = Comment.objects.filter(article=article).order_by('-created_on')

        # Comment form for logged-in users
        context['comment_form'] = CommentForm()

        # If the logged-in user is the author of the article, add an edit link
        if self.request.user.profile == article.author:
            context['edit_link'] = True

       # Previous and Next articles based on creation time
        context['previous_article'] = Article.objects.filter(
            created_on__lt=article.created_on
        ).order_by('-created_on').first()

        context['next_article'] = Article.objects.filter(
            created_on__gt=article.created_on
        ).order_by('created_on').first()

        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            # Get the Profile instance associated with the logged-in User
            user_profile = Profile.objects.get(user=request.user)

            # Save the comment
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = user_profile  # Use Profile instance here
            comment.save()

        return redirect('blog:article_detail', pk=article.pk)  # Redirect to the same article page after posting

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'article_add.html'

    def form_valid(self, form):
        # Save the logged-in user's profile as the author
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:article_list')  # Corrected to use reverse_lazy for success URL

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'category', 'entry', 'header_image']
    template_name = 'article_edit.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user.profile == article.author

    def get_success_url(self):
        return reverse_lazy('blog:article_detail', kwargs={'pk': self.object.pk})  # Corrected to use reverse_lazy for redirect
