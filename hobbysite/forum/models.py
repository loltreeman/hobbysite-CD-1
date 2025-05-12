from django.db import models
from user_management.models import Profile

class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = "Thread Category"
        verbose_name_plural = "Thread Categories"

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ThreadCategory, on_delete=models.SET_NULL, null=True, blank=True)
    entry = models.TextField()
    header_image = models.ImageField(upload_to='thread/images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"