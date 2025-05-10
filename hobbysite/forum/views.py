from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Thread, ThreadCategory, Comment
from .forms import CommentForm, ThreadCreateForm, ThreadUpdateForm

class ThreadListView(LoginRequiredMixin, ListView):
    pass

class ThreadDetailView(LoginRequiredMixin, DetailView):
    pass

class ThreadCreateView(LoginRequiredMixin, CreateView):
    pass

class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass