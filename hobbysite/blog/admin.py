from django.contrib import admin
from django.contrib.auth.models import User
from .models import ArticleCategory, Article, Comment, Profile  # Assuming Profile is related to Article as well

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ['name',]  
    search_fields = ['name',]  
    ordering = ['name']  


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ['title', 'category', 'created_on', 'updated_on',]  
    list_filter = ['category', 'created_on']  
    search_fields = ['title', 'content',]  
    ordering = ['-created_on']  

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['author', 'article', 'created_on']  
    list_filter = ['created_on']  
    search_fields = ['entry']  
    ordering = ['created_on']  


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]  


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(User)  
admin.site.register(User, CustomUserAdmin)
