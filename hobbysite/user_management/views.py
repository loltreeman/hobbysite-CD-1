from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProfileForm

@login_required
def profile_dashboard(request):
    return render(request, 'user_management/profile_dashboard.html', {
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
    return render(request, 'user_management/profile_update.html', {'form': form})

# (Optional) A simple registration view if custom signup is needed
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create associated profile
            Profile.objects.create(user=user, display_name=user.username)
            return redirect('login')
    return render(request, 'user_management/register.html', {'form': form})