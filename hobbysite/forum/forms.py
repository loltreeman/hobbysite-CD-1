from django import forms
from .models import Thread, Comment

class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'entry', 'header_image']

class ThreadUpdateForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ['created_on', 'author']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']