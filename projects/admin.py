from django.contrib import admin
from projects.models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "get_participants", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__email")
    raw_id_fields = ("owner",)
    filter_horizontal = ("participants",)

    @admin.display(description="Участники проекта")
    def get_participants(self, obj):
        return ", ".join([user.email for user in obj.participants.all()])
