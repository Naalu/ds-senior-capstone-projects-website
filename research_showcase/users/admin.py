from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "role",
        "department",
        "profile_complete",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "profile_complete", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "department")}),
        ("Status", {"fields": ("profile_complete", "last_activity")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "role")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "department",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username", "email", "department")
    ordering = ("username",)
    readonly_fields = ("last_activity",)


admin.site.register(User, CustomUserAdmin)
