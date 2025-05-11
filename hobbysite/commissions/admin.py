from django.contrib import admin
from .models import Commission, Job


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ("title", "status", "created_on", "updated_on", "author")
    search_fields = ("title", "description")
    list_filter = ("status",)

class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ("status", "commission", "manpower_required", "role")
    search_fields = ("title", "description")
    list_filter = ("status",)

admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)



