from django.contrib import admin
from .models import ThreadCategory, Thread, Comment

class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    list_display = ('name', 'description')

class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    list_display = ('title', 'category', 'author', 'created_on', 'updated_on')

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('thread', 'author', 'created_on', 'updated_on')

admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)