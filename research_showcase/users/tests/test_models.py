from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Notification, create_in_app_notification

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


class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="notifyuser", password="password123"
        )

    def test_create_notification(self):
        notification = Notification.objects.create(
            recipient=self.user, message="Test Notification"
        )
        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.message, "Test Notification")
        self.assertFalse(notification.read)
        self.assertIsNone(notification.link)
        self.assertEqual(
            str(notification), "Notification for notifyuser: Test Notification..."
        )

    def test_notification_ordering(self):
        Notification.objects.create(recipient=self.user, message="First")
        Notification.objects.create(recipient=self.user, message="Second")
        notifications = Notification.objects.filter(recipient=self.user)
        self.assertEqual(notifications.first().message, "Second")  # Newest first

    def test_create_in_app_notification_helper_enabled(self):
        self.user.notify_in_app_on_status_change = True
        self.user.save()
        create_in_app_notification(self.user, "Helper Test 1", link="/test-link")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.message, "Helper Test 1")
        self.assertEqual(notification.link, "/test-link")

    def test_create_in_app_notification_helper_disabled(self):
        self.user.notify_in_app_on_status_change = False
        self.user.save()
        create_in_app_notification(self.user, "Helper Test 2")
        self.assertEqual(Notification.objects.count(), 0)
