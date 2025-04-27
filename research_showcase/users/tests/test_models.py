from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..models import Notification, User, create_in_app_notification

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_faculty_user(self):
        user = User.objects.create_user(
            username="facultytest",
            password="password123",
            email="faculty@test.com",
            role="faculty",
        )
        self.assertEqual(user.username, "facultytest")
        self.assertEqual(user.role, "faculty")
        self.assertTrue(user.is_faculty())
        self.assertFalse(user.is_admin())
        self.assertTrue(user.can_submit_research())
        self.assertFalse(user.can_review_research())

    def test_create_admin_user(self):
        user = User.objects.create_user(
            username="admintest",
            password="password123",
            email="admin@test.com",
            role="admin",
        )
        self.assertEqual(user.username, "admintest")
        self.assertEqual(user.role, "admin")
        self.assertFalse(user.is_faculty())
        self.assertTrue(user.is_admin())
        self.assertTrue(user.can_submit_research())
        self.assertTrue(user.can_review_research())

    def test_default_role_is_faculty(self):
        user = User.objects.create_user(
            username="defaulttest", password="password123", email="default@test.com"
        )
        # Assuming 'faculty' is the default based on models.py
        self.assertEqual(user.role, "faculty")
        self.assertTrue(user.is_faculty())

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="password", email="test@example.com"
        )

    def test_update_last_activity(self):
        """Test the update_last_activity method sets the timestamp."""
        initial_activity = self.user.last_activity
        self.assertIsNone(initial_activity)  # Should be None initially

        # Simulate some time passing
        # timezone.now() might be too close, let's ensure a small delay or mock time if needed
        # For simplicity, just call it
        self.user.update_last_activity()
        self.user.refresh_from_db()

        self.assertIsNotNone(self.user.last_activity)
        # Check if it's a recent timestamp (within a reasonable threshold)
        self.assertTrue((timezone.now() - self.user.last_activity).total_seconds() < 5)


class NotificationModelTests(TestCase):
    def test_create_notification(self):
        """Test notification creation via model directly."""
        Notification.objects.create(recipient=self.user, message="Test 1")
        self.assertEqual(self.user.notifications.count(), 1)
        self.assertEqual(self.user.notifications.first().message, "Test 1")

    def test_create_in_app_notification_helper_enabled(self):
        """Test helper function creates notification when user preference is True."""
        # Ensure preference is True (should be default if not set in setUpTestData)
        self.user.notify_in_app_on_status_change = True
        self.user.save()
        create_in_app_notification(self.user, "Helper Test 1")
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().recipient, self.user)

    def test_create_in_app_notification_helper_disabled(self):
        """Test helper function does not create notification when preference is False."""
        self.user.notify_in_app_on_status_change = False
        self.user.save()
        create_in_app_notification(self.user, "Helper Test 2")
        self.assertEqual(Notification.objects.count(), 0)

    def test_notification_ordering(self):
        """Test notifications are ordered by timestamp descending."""
        Notification.objects.create(recipient=self.user, message="First")
        # Ensure timestamp difference
        import time

        time.sleep(0.01)
        Notification.objects.create(recipient=self.user, message="Second")
        notifications = self.user.notifications.all()
        self.assertEqual(notifications[0].message, "Second")
        self.assertEqual(notifications[1].message, "First")

    @classmethod
    def setUpTestData(cls):
        # Create user once for the class
        cls.user = User.objects.create_user(
            username="notifyuser", password="password", email="notify@example.com"
        )

    def test_notification_str_method(self):
        """Test the __str__ method of the Notification model."""
        message_text = (
            "This is a test notification message that is quite long to test truncation."
        )
        notification = Notification.objects.create(
            recipient=self.user, message=message_text
        )
        expected_str = f"Notification for {self.user.username}: {message_text[:50]}..."
        self.assertEqual(str(notification), expected_str)

    def test_notification_str_method_short_message(self):
        """Test the __str__ method with a short message."""
        message_text = "Short message."
        notification = Notification.objects.create(
            recipient=self.user, message=message_text
        )
        # Expect no ellipsis for short messages
        expected_str = f"Notification for {self.user.username}: {message_text}"
        self.assertEqual(str(notification), expected_str)
