from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User  # Import the custom user model


# Extend UserAdmin to use Django's built-in admin features for Users
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email",)}),
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
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


# Register the custom User model with Django Admin
admin.site.register(User, CustomUserAdmin)
