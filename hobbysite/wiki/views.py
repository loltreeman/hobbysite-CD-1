from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, ArticleCategory
from .forms import CreateArticleForm, UpdateArticleForm, CommentForm
from user_management.models import Profile


class ArticleListView(ListView):
    model = Article
    template_name = "wiki/article_list.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            try:
                profile = user.profile
                user_articles = Article.objects.filter(author=profile).order_by("category__name", "title")
                all_articles = Article.objects.exclude(author=profile).order_by("category__name", "title")
            except Profile.DoesNotExist:
                user_articles = None
                all_articles = Article.objects.all().order_by("category__name", "title")
        else:
            user_articles = None
            all_articles = Article.objects.all().order_by("category__name", "title")

        grouped_articles = {}
        for article in all_articles:
            category_name = article.category.name if article.category else "Uncategorized"
            grouped_articles.setdefault(category_name, []).append(article)

        context["user_articles"] = user_articles
        context["grouped_articles"] = grouped_articles
        context["create_article_url"] = reverse_lazy("wiki:article_create") 

        return context
    
class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = "wiki/article_detail.html"
    context_object_name = "article"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("wiki:article_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        context["related_articles"] = Article.objects.filter(
            category=article.category
        ).exclude(pk=article.pk)[:2]

        context["comments"] = article.wiki_comments.order_by("-created_on")  # Correct related name for comments
        if self.request.user.is_authenticated:
            context["form"] = self.get_form()
        else:
            context["form"] = None

        user = self.request.user
        context["is_owner"] = user.is_authenticated and hasattr(user, "profile") and article.author == user.profile

        context["back_to_list_url"] = reverse("wiki:article_list")

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            if request.user.is_authenticated and hasattr(request.user, "profile"):
                comment = form.save(commit=False)
                comment.article = self.object
                comment.author = request.user.profile
                comment.save()
                return redirect(self.get_success_url())
            else:
                return redirect("login")
        return self.form_invalid(form)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = CreateArticleForm
    template_name = "wiki/article_create.html"
    success_url = reverse_lazy("wiki:article_list")

    def form_valid(self, form):
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            return redirect("login")  
        form.instance.author = profile
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["category"].queryset = ArticleCategory.objects.all()
        return form
    

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = UpdateArticleForm
    template_name = "wiki/article_update.html"

    def get_success_url(self):
        return reverse("wiki:article_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            return redirect("login")  
        form.instance.author = profile  # Ensuring the author field is not modified
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["category"].queryset = ArticleCategory.objects.all()  
        return form
