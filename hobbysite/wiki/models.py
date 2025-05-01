from django.db import models
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from user_management.models import Profile

# Create your models here.

class ArticleCategory(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'


class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        'ArticleCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='articles'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    header_image = models.ImageField(upload_to='images/', blank=True, null=True)  # Ensure this field exists
    author = models.ForeignKey(
        'user_management.Profile', on_delete=models.SET_NULL, null=True, related_name='articles'
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
           return reverse('wiki:wiki-detail', args=[self.pk])
    

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

class Comment(models.Model):
    author = models.ForeignKey('user_management.Profile', on_delete = models.SET_NULL, null = True, related_name = 'comments')
    article = models.ForeignKey('Article', on_delete = models.CASCADE, related_name = 'comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['created_on']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.author.user.profile} in {self.article.title}"