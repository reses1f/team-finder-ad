from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.forms import UserChangeForm, UserCreationForm
from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ("email", "name", "surname", "phone", "projects_count", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "name", "surname", "phone")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Профиль", {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Избранное", {"fields": ("favorites",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2"),
            },
        ),
    )
    filter_horizontal = ("favorites", "groups", "user_permissions")

    @admin.display(description="Кол-во проектов")
    def projects_count(self, obj):
        return obj.projects.count()

