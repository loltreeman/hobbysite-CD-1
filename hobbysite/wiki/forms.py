from django import forms
from .models import Article, Comment


class UploadArticleImageForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["header_image"]


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["created_on", "updated_on", "author"]


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["created_on", "author"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["created_on", "updated_on", "author", "article"]