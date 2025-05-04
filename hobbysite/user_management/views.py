from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

@login_required
def homepage(request):
    """
    Landing page listing all your apps. Redirect target after login.
    """
    apps = [
        {'label': 'My Profile',      'url': 'user_management:profile_dashboard'},
        {'label': 'Blog Articles',   'url': 'blog:article_list'},
        {'label': 'Forum Threads',   'url': 'forum:threadList'},
        {'label': 'Store Items',     'url': 'merchstore:merch_list'},
        {'label': 'Wiki Articles',   'url': 'wiki:articles_list'},
        {'label': 'Commissions',     'url': 'commissions:commissions_list'},
    ]
    return render(request, 'homepage.html', {'apps': apps})

@login_required
def profile_dashboard(request):
    return render(request, 'profile.html', {
        'user': request.user,
        'update_link': reverse_lazy('user_management:profile_update')
    })

@login_required
def profile_update(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_management:profile_dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', {'form': form})

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, display_name=user.username)
            return redirect('login')
    return render(request, 'register.html', {'form': form})

