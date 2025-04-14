from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .forms import NotificationPreferenceForm
from .models import Notification, create_in_app_notification

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


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.faculty_user = User.objects.create_user(
            username="facultyview",
            password="password123",
            email="fv@test.com",
            role="faculty",
        )
        self.admin_user = User.objects.create_user(
            username="adminview",
            password="password123",
            email="av@test.com",
            role="admin",
            is_staff=True,  # Need staff for admin access typically
            is_superuser=True,  # And superuser for /admin/
        )
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.edit_profile_url = reverse("edit_profile")
        self.mark_read_url = reverse("mark_notifications_read")
        self.home_url = reverse("home")
        self.admin_index_url = "/admin/"  # Hardcoded as admin:index isn't default

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post_success_faculty(self):
        response = self.client.post(
            self.login_url, {"username": "facultyview", "password": "password123"}
        )
        # Redirects to submit_research for faculty
        self.assertRedirects(response, reverse("submit_research"))
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_view_post_success_admin(self):
        response = self.client.post(
            self.login_url, {"username": "adminview", "password": "password123"}
        )
        # Redirects to admin index for superuser/admin
        self.assertRedirects(response, self.admin_index_url)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_view_post_success_with_next(self):
        next_url = self.edit_profile_url
        response = self.client.post(
            f"{self.login_url}?next={next_url}",
            {"username": "facultyview", "password": "password123"},
        )
        self.assertRedirects(response, next_url)

    def test_login_view_post_fail(self):
        response = self.client.post(
            self.login_url, {"username": "facultyview", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)  # Stays on login page
        self.assertTemplateUsed(response, "users/login.html")
        self.assertFalse("_auth_user_id" in self.client.session)
        self.assertContains(response, "Invalid username or password")

    def test_logout_view(self):
        self.client.login(username="facultyview", password="password123")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_edit_profile_view_get_unauthenticated(self):
        response = self.client.get(self.edit_profile_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.edit_profile_url}")

    def test_edit_profile_view_get_authenticated(self):
        self.client.login(username="facultyview", password="password123")
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/edit_profile.html")
        self.assertIsInstance(response.context["form"], NotificationPreferenceForm)

    def test_edit_profile_view_post_success(self):
        self.client.login(username="facultyview", password="password123")
        self.assertTrue(
            self.faculty_user.notify_by_email_on_status_change
        )  # Default is True
        self.assertTrue(
            self.faculty_user.notify_in_app_on_status_change
        )  # Default is True

        response = self.client.post(
            self.edit_profile_url,
            {
                "notify_by_email_on_status_change": False,
                # Missing key defaults to False for checkboxes
                # "notify_in_app_on_status_change": False
            },
            follow=True,  # Follow redirect
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/edit_profile.html")
        self.assertContains(response, "preferences have been updated")

        self.faculty_user.refresh_from_db()
        self.assertFalse(self.faculty_user.notify_by_email_on_status_change)
        self.assertFalse(self.faculty_user.notify_in_app_on_status_change)

    def test_mark_notifications_read_view_unauthenticated(self):
        response = self.client.post(self.mark_read_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_mark_notifications_read_view_get_fail(self):
        self.client.login(username="facultyview", password="password123")
        response = self.client.get(self.mark_read_url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_mark_notifications_read_view_post_success(self):
        self.client.login(username="facultyview", password="password123")
        Notification.objects.create(recipient=self.faculty_user, message="Unread 1")
        Notification.objects.create(
            recipient=self.faculty_user, message="Unread 2", read=True
        )
        Notification.objects.create(recipient=self.faculty_user, message="Unread 3")

        self.assertEqual(
            Notification.objects.filter(
                recipient=self.faculty_user, read=False
            ).count(),
            2,
        )

        response = self.client.post(self.mark_read_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True, "marked_read_count": 2})
        self.assertEqual(
            Notification.objects.filter(
                recipient=self.faculty_user, read=False
            ).count(),
            0,
        )


class NotificationPreferenceFormTests(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "notify_by_email_on_status_change": True,
            "notify_in_app_on_status_change": False,
        }
        form = NotificationPreferenceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_checkbox_widgets(self):
        form = NotificationPreferenceForm()
        self.assertIn(
            'class="form-check-input"',
            form.fields["notify_by_email_on_status_change"].widget.render(
                "notify_by_email_on_status_change", True
            ),
        )
        self.assertIn(
            'class="form-check-input"',
            form.fields["notify_in_app_on_status_change"].widget.render(
                "notify_in_app_on_status_change", True
            ),
        )


# Remove the placeholder comment
# Create your tests here.
