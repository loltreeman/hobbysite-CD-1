from django.contrib import admin
from .models import Commission, Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ("title", "peopleRequired", "createdOn", "updatedOn")
    search_fields = ("title", "description")
    list_filter = ("createdOn", "updatedOn")
    ordering = ("createdOn",)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ("commission", "entry", "createdOn", "updatedOn")
    search_fields = ("entry", "commission__title")
    list_filter = ("createdOn", "updatedOn")
    ordering = ("-createdOn",)


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)
