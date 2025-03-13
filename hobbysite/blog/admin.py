from django.contrib import admin
from .models import ArticleCategory, Article

# Register your models here.
class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ['name',]
    search_display = ['name',]
    ordering = ['name']

class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ['title', 'category', 'created_on', 'updated_on',]
    list_filter = ['category', 'created_on']
    search_fields = ['title', 'content',]
    ordering = ['-created_on']

admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)

