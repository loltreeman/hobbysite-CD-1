from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Custom Profile model linked to built-in User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    name = models.TextField(max_length=50, blank=True)
    user_bio = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.name or self.user.username  # Fallback if name is blank

# Article Category model
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'

    def __str__(self):
        return self.name

# Article model with foreign keys to Profile and Category
class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='articles')
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, related_name='articles')
    entry = models.TextField()
    header_image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.pk})

# Comment model with FK to Profile and Article
class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'

# Article Image model for image gallery
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')  # Link to Article
    image = models.ImageField(upload_to='blog/images/')  # Store images in 'blog/images' folder
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for each image
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Image for {self.article.title}"
