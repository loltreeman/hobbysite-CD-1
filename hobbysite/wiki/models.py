from django.db import models

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    descriptiom = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory, 
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    entry = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdOn']
        
    def __str__(self):
        return self.title

