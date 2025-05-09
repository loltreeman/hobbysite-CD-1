from django.contrib import admin
from .models import ArticleCategory, Article, Comment

# Register your models here.

class ArticleInLine(admin.TabularInline):
    model = Article

class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInLine,]

    search_fields = ['name',]
    list_display = ['name',]
    list_filter = ['name',]


class ArticleAdmin(admin.ModelAdmin):
    model = Article

    search_fields = ['title',]
    list_display = ['title', 'category']
    list_filter = ['title',]

    def save_model(self, request, obj, form, change):
        obj.author = request.user.profile
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    model = Comment

    search_fields = ['author__username', ]
    list_display = ['author', 'article', ]
    list_filter = ['author', ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user.profile
        super().save_model(request, obj, form, change)


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)