from django.conf import settings  # To link recipient to User model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    This model implements a role-based system with two primary roles:
    - Faculty: Can submit research projects
    - Admin: Can review and approve/reject research projects in addition to faculty privileges
    """

    ROLE_CHOICES = [
        ("faculty", "Faculty"),
        ("admin", "Admin"),
    ]
    role: models.CharField = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="faculty"
    )

    # Additional profile fields
    department: models.CharField = models.CharField(max_length=100, blank=True)
    profile_complete: models.BooleanField = models.BooleanField(default=False)
    last_activity: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    # Notification Preferences
    notify_by_email_on_status_change: models.BooleanField = models.BooleanField(
        default=True
    )
    notify_in_app_on_status_change: models.BooleanField = models.BooleanField(
        default=True
    )

    def is_faculty(self):
        return self.role == "faculty"

    def is_admin(self):
        return self.role == "admin"

    def can_submit_research(self):
        """Check if user can submit research projects"""
        return self.is_faculty() or self.is_admin()

    def can_review_research(self):
        """Check if user can review and approve/reject submissions"""
        return self.is_admin()

    def update_last_activity(self):
        """Update the last activity timestamp"""
        self.last_activity = timezone.now()
        self.save(update_fields=["last_activity"])


# Add the missing Notification model
class Notification(models.Model):
    recipient: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message: models.TextField = models.TextField()
    read: models.BooleanField = models.BooleanField(default=False)
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    link: models.URLField = models.URLField(blank=True, null=True)  # Optional link for the notification

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:50]}..."

    class Meta:
        ordering = ["-timestamp"]  # Show newest first


def create_in_app_notification(user, message, link=None):
    """
    Creates an in-app notification for the specified user if they have opted in.
    """
    if user and user.notify_in_app_on_status_change:
        try:
            Notification.objects.create(recipient=user, message=message, link=link)
            print(
                f"In-app notification created for {user.username}: {message[:30]}..."
            )  # Log creation
        except Exception as e:
            # Log the error - replace print with proper logging in production
            print(f"ERROR creating in-app notification for {user.username}: {e}")
