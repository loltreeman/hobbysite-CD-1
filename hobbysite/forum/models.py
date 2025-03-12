from django.db import models

class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Post Categories"
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, null=True, blank=True)
    entry = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-createdOn']
    
    def __str__(self):
        return self.title