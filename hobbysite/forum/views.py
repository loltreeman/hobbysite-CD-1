from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from forum.models import Thread, ThreadCategory, Comment
from forum.forms import CommentForm, ThreadCreateForm, ThreadUpdateForm
from user_management.models import Profile

class ThreadListView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'forum/thread_list.html'
    context_object_name = 'all_threads'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Thread.objects.exclude(author=profile).select_related('category').order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        user_threads = Thread.objects.filter(author=profile).order_by('-created_on')

        grouped_user_threads = {}
        for thread in user_threads:
            grouped_user_threads.setdefault(thread.category, []).append(thread)

        grouped_all_threads = {}
        for thread in context['all_threads']:
            grouped_all_threads.setdefault(thread.category, []).append(thread)

        context['user_threads'] = user_threads
        context['grouped_user_threads'] = grouped_user_threads  
        context['grouped_all_threads'] = grouped_all_threads  
        context['all_categories'] = ThreadCategory.objects.all()

        return context


class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.object
        profile = Profile.objects.get(user=self.request.user)

        context['related_threads'] = Thread.objects.filter(
            category=thread.category
        ).exclude(pk=thread.pk)[:2]
        
        context['comments'] = Comment.objects.filter(thread=thread).order_by('created_on')
        context['comment_form'] = CommentForm()
        
        if thread.author == profile:
            context['edit_link'] = True

        context['previous_thread'] = Thread.objects.filter(
            created_on__lt=thread.created_on
        ).order_by('-created_on').first()
        
        context['next_thread'] = Thread.objects.filter(
            created_on__gt=thread.created_on
        ).order_by('created_on').first()

        return context

    def post(self, request, *args, **kwargs):
        thread = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = Profile.objects.get(user=request.user)
            comment.thread = thread
            comment.save()
        return redirect('forum:thread_detail', pk=thread.pk)

class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadCreateForm
    template_name = 'forum/thread_create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = ThreadCategory.objects.all()
        return form

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()

        new_category_name = post_data.get('new_category')
        if new_category_name:
            category, created = ThreadCategory.objects.get_or_create(name=new_category_name.strip())
            post_data['category'] = category.id

        self.request.POST = post_data
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:thread_list')

class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    form_class = ThreadUpdateForm
    template_name = 'forum/thread_update.html'

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user)
        return self.get_object().author == profile

    def get_success_url(self):
        return reverse_lazy('forum:thread_detail', kwargs={'pk': self.object.pk})