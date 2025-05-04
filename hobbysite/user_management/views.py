from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

@login_required
def profile_dashboard(request):
    return render(request, 'profile.html', {
        'user': request.user,
        'update_link': reverse_lazy('user_management:profile_update')
    })

@login_required
def profile_update(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_management:profile_dashboard')
    return render(request, 'profile_update.html', {'form': form})

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create associated profile
            Profile.objects.create(user=user, display_name=user.username)
            return redirect('login')
    return render(request, 'register.html', {'form': form})

