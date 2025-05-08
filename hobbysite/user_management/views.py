from django.shortcuts import render

# Create your views here.


from django.views.generic.edit import UpdateView, CreateView
from .models import Profile
from .forms import ProfileUpdateForm, ProfileCreateForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile_update.html'
    success_url = '/homepage'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'profile_create.html'
    success_url = '/homepage'


class DashboardView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'dashboard.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_create.html'
    success_url = '/homepage'