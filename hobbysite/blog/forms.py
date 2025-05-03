from django import forms
from .models import Article, Comment, ArticleCategory

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image']

class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        # Exclude 'created_on' and 'author' as they should not be editable
        exclude = ['created_on', 'author'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
