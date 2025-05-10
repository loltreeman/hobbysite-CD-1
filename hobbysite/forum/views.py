from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from forum.models import Thread, ThreadCategory, Comment
from forum.forms import CommentForm, ThreadCreateForm, ThreadUpdateForm
from user_management.models import Profile

class ThreadListView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'thread_list.html'
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
        context['grouped_user_threads'] = grouped_user_threads.items()
        context['grouped_all_threads'] = grouped_all_threads.items()
        context['all_categories'] = ThreadCategory.objects.all()

        return context

class ThreadDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = 'thread_detail.html'
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
    template_name = 'thread_create.html'

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:thread_list')

class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    form_class = ThreadUpdateForm
    template_name = 'thread_update.html'

    def test_func(self):
        profile = Profile.objects.get(user=self.request.user)
        return self.get_object().author == profile

    def get_success_url(self):
        return reverse_lazy('forum:thread_detail', kwargs={'pk': self.object.pk})