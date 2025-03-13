from django.db import models
from django.urls import reverse 

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        # Included so it appears as 'Article Category' instead of 'Article category' in some cases on the admin panel.
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, related_name="article_category")
    entry = models.TextField()
    image_url = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    # Articles should be sorted by the date it was created, in descending order
    class Meta:
        ordering = ['-created_on']
        # Included so it appears as 'Article' instead of 'article' in some cases on the admin panel.
        verbose_name = 'Article' 
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:article_detail", args=[str(self.pk)])
