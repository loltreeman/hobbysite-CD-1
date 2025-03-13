from django.contrib import admin
from .models import PostCategory, Post

class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    list_display = ('name', 'description')
    ordering = ['name']

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'category__name', 'created_on', 'updated_on')
    ordering = ['-created_on']

admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)