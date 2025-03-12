from django.db import models
from django.urls import reverse 

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Article Categories'

    def __str__(self):
        return self.name

