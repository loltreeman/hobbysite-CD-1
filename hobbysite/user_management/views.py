from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

@login_required
def homepage(request):
    return render(request, 'registration/homepage.html')

@login_required
def profile_dashboard(request):
    return render(request, 'registration/profile.html', {
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
    return render(request, 'registration/profile_update.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            Profile.objects.create(user=user, display_name=user.username, email=user.email)
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
