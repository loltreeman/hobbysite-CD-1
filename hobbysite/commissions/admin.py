from django.contrib import admin
from .models import Commission, Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ("title", "people_required", "created_on", "updated_on")
    search_fields = ("title", "description")
    list_filter = ("created_on", "updated_on")
    ordering = ("created_on",)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ("commission", "entry", "created_on", "updated_on")
    search_fields = ("entry", "commission__title")
    list_filter = ("created_on", "updated_on")
    ordering = ("-created_on",)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)
