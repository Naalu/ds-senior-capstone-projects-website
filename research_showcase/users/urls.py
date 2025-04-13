from django.contrib.auth import views as auth_views
from django.urls import path

from .views import edit_profile, login_view, logout_view, mark_notifications_read

urlpatterns = [
    # Authentication URLs
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # Password Reset URLs (Django's built-in views)
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Add the URL for editing profile/preferences
    path("profile/", edit_profile, name="edit_profile"),
    # Add the URL for marking notifications read
    path(
        "notifications/mark-read/",
        mark_notifications_read,
        name="mark_notifications_read",
    ),
]
