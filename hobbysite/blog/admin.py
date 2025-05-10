from django.contrib import admin
from django.contrib.auth.models import User
from .models import ArticleCategory, Article, Comment, Profile  # Assuming Profile is related to Article as well

# Register your models here.

# Inline for Profile (if applicable)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Admin for ArticleCategory
class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ['name',]  # Fields to display in the admin list
    search_fields = ['name',]  # Fields to search for in the admin
    ordering = ['name']  # Ordering of the rows in the admin

# Admin for Article
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ['title', 'category', 'created_on', 'updated_on',]  # Columns to display in list view
    list_filter = ['category', 'created_on']  # Filters available in the sidebar
    search_fields = ['title', 'content',]  # Searchable fields
    ordering = ['-created_on']  # Ordering by created_on descending

# Admin for Comment
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['author', 'article', 'created_on']  # Columns to display in list view
    list_filter = ['created_on']  # Filters available in the sidebar
    search_fields = ['entry']  # Fields to search for in the admin
    ordering = ['created_on']  # Ordering by creation date

# If Profile is connected to User (through an inline)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]  # Add Profile inline if user has a related Profile

# Register models in admin
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(User)  # Unregister the default User model
admin.site.register(User, CustomUserAdmin)  # Register CustomUserAdmin if you have a custom User model
