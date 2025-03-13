from django.contrib import admin
from .models import Article, ArticleCategory


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [ArticleInline]


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'category__name')
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category', 'created_on', 'updated_on')
    ordering = ('-created_on',)


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)