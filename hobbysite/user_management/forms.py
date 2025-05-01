from django import forms

from .models import Profile, User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 
        "display_name", 
        "email_address"
        ]


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']