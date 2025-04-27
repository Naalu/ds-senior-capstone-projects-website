from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..models import ResearchProject, StatusHistory
from ..views import approve_research  # Needed for the mock test

User = get_user_model()


class ResearchViewTests(TestCase):
    def setUp(self):
        # Create test users
        self.faculty_user = User.objects.create_user(
            username="faculty",
            email="faculty@example.com",
            password="facultypass123",
            role="faculty",
        )

        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            role="admin",
        )

        # Create test project
        self.project = ResearchProject.objects.create(
            title="Test Research Project",
            abstract="This is a test abstract for a research project.",
            author=self.faculty_user,
            student_author_name="Test Student",
            approval_status="pending",
        )

        self.client = Client()

    def test_submit_research_view_requires_faculty(self):
        """Test that submit view requires faculty login"""
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Login as faculty
        self.client.login(username="faculty", password="facultypass123")
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 200)  # Should now be accessible

    def test_review_research_view_requires_admin(self):
        """Test that review view requires admin login"""
        # Login as faculty (shouldn't have access)
        self.client.login(username="faculty", password="facultypass123")
        response = self.client.get(reverse("review_research"))
        self.assertEqual(response.status_code, 403)  # Should return Forbidden

        # Login as admin
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("review_research"))
        self.assertEqual(response.status_code, 200)  # Should now be accessible

    def test_search_research_view(self):
        """
        Test the search functionality for research projects.

        Verifies that:
        1. Searches return projects with matching terms in title or abstract
        2. Searches only return approved projects
        3. Non-matching searches return no results
        """
        # Create an approved project
        ResearchProject.objects.create(
            title="Machine Learning Analysis",
            abstract="A study of machine learning algorithms",
            author=self.faculty_user,
            student_author_name="ML Researcher",
            approval_status="approved",
            date_presented=date.today(),
        )

        # Test search with matching term
        response = self.client.get(reverse("search_research"), {"q": "machine"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Machine Learning Analysis")

        # Test search with non-matching term
        response = self.client.get(reverse("search_research"), {"q": "quantum"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Machine Learning Analysis")


class ResearchSubmissionViewTest(TestCase):
    def setUp(self):
        # Create test users
        self.faculty_user = User.objects.create_user(
            username="faculty_sub", password="testpassword", role="faculty"
        )
        self.admin_user = User.objects.create_user(
            username="admin_sub", password="testpassword", role="admin"
        )
        self.client = Client()

    def test_faculty_access(self):
        """Test faculty can access the submission page."""
        self.client.login(username="faculty_sub", password="testpassword")
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 200)

    def test_admin_access(self):
        """Test admin cannot access the submission page (should redirect or forbid)."""
        self.client.login(username="admin_sub", password="testpassword")
        response = self.client.get(reverse("submit_research"))
        # Assuming redirection to dashboard or 403 Forbidden based on decorator
        self.assertIn(response.status_code, [302, 403])

    def test_unauthorized_access(self):
        """Test anonymous users are redirected to login."""
        response = self.client.get(reverse("submit_research"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('submit_research')}"
        )


class ResearchReviewProcessTest(TestCase):
    def setUp(self):
        # Create test users
        self.faculty_user = User.objects.create_user(
            username="faculty_rev", password="password", role="faculty"
        )
        self.admin_user = User.objects.create_user(
            username="admin_rev", password="password", role="admin"
        )

        # Create project needing review
        self.project_pending = ResearchProject.objects.create(
            title="Project For Review",
            abstract="Pending abstract",
            author=self.faculty_user,
            student_author_name="Review Student",
            approval_status="pending",
            github_link="https://example.com",
            video_link="https://example.com/video",
        )
        # Create file attachments for the project
        self.pdf_file = SimpleUploadedFile(
            "test.pdf", b"pdf content", content_type="application/pdf"
        )
        self.project_pending.pdf_file.save("test.pdf", self.pdf_file, save=True)

        self.client = Client()
        self.client.login(username="admin_rev", password="password")

    def test_review_page_shows_new_fields(self):
        """Test review page displays new fields like GitHub/video links."""
        response = self.client.get(reverse("review_research"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project_pending.title)
        self.assertContains(response, "https://example.com")  # GitHub link
        self.assertContains(response, "https://example.com/video")  # Video link

    def test_approve_project(self):
        """Test approving a project updates its status and creates history."""
        response = self.client.get(
            reverse("approve_research", args=[self.project_pending.id]), follow=True
        )
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(response, "has been approved and published")
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "approved")
        self.assertTrue(
            StatusHistory.objects.filter(
                project=self.project_pending, status_to="approved"
            ).exists()
        )

    def test_reject_project_get_form(self):
        """Test GET request for reject project form shows the form."""
        response = self.client.get(
            reverse("reject_research", args=[self.project_pending.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reason for Rejection")

    def test_reject_project_post(self):
        """Test rejecting a project updates status and creates history."""
        reject_url = reverse("reject_research", args=[self.project_pending.id])
        response = self.client.post(
            reject_url, {"reason": "Incomplete abstract"}, follow=True
        )
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(response, "has been rejected")
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "rejected")
        history = StatusHistory.objects.filter(
            project=self.project_pending, status_to="rejected"
        )
        self.assertTrue(history.exists())
        self.assertEqual(history.first().comment, "Incomplete abstract")

    def test_request_revision_get_form(self):
        """Test GET request for request revision form shows the form."""
        response = self.client.get(
            reverse("request_revision", args=[self.project_pending.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reason for Revision Request")

    def test_request_revision_post(self):
        """Test requesting revision updates status and creates history."""
        revision_url = reverse("request_revision", args=[self.project_pending.id])
        response = self.client.post(
            revision_url, {"reason": "Update abstract"}, follow=True
        )
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(response, "Revision requested")
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "needs_revision")
        history = StatusHistory.objects.filter(
            project=self.project_pending, status_to="needs_revision"
        )
        self.assertTrue(history.exists())
        self.assertEqual(history.first().comment, "Update abstract")


class MultiStepFormTest(TestCase):
    def setUp(self):
        # Create a faculty user for testing
        self.faculty_user = User.objects.create_user(
            username="faculty_form", password="password", role="faculty"
        )
        self.client = Client()
        self.client.login(username="faculty_form", password="password")

    def test_form_navigation(self):
        """Test navigation through the multi-step form using the client."""
        # Access the first step
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Step 1: Basic Information")

        # Post data for step 1 (example minimal valid data)
        step_1_data = {
            "submit_research_wizard-current_step": "step1",
            "step1-title": "Multi-Step Project",
            "step1-abstract": "This abstract must be long enough for validation. Example text to meet length requirement.",
            "step1-student_author_name": "Form Student",
        }
        response = self.client.post(reverse("submit_research"), step_1_data)
        # Successful post should redirect to the same URL (GET for next step)
        self.assertEqual(
            response.status_code, 200
        )  # Django FormWizard returns 200 for next step
        self.assertContains(response, "Step 2: Project Details")


class SuccessPageTest(TestCase):
    def setUp(self):
        # Create a faculty user for testing
        self.faculty_user = User.objects.create_user(
            username="faculty_success", password="password", role="faculty"
        )
        self.client = Client()
        self.client.login(username="faculty_success", password="password")

    def test_success_page_accessible(self):
        """Test that the submission success page is accessible after submission (simulated)."""
        # Note: Direct access might be restricted, test assumes flow from submission
        # This test primarily ensures the URL exists and template renders.
        response = self.client.get(reverse("submission_success"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submission Successful")


class FacultyViewsTest(TestCase):
    def setUp(self):
        self.faculty1 = User.objects.create_user(
            username="faculty1", password="password", role="faculty"
        )
        self.faculty2 = User.objects.create_user(
            username="faculty2", password="password", role="faculty"
        )
        self.project1 = ResearchProject.objects.create(
            title="Faculty 1 Project 1",
            abstract="Abstract 1",
            author=self.faculty1,
            student_author_name="Student A",
            approval_status="approved",
            date_presented=date(2024, 1, 1),
        )
        self.project2 = ResearchProject.objects.create(
            title="Faculty 1 Project 2 Needs Revision",
            abstract="Abstract 2",
            author=self.faculty1,
            student_author_name="Student B",
            approval_status="needs_revision",
        )
        self.project3 = ResearchProject.objects.create(
            title="Faculty 2 Project",
            abstract="Abstract 3",
            author=self.faculty2,
            student_author_name="Student C",
            approval_status="pending",
        )
        # Add history for project 2
        StatusHistory.objects.create(
            project=self.project2,
            status_from="pending",
            status_to="needs_revision",
            comment="Please update abstract",
        )

        self.client = Client()
        self.client.login(username="faculty1", password="password")

    def test_my_submissions_view_get(self):
        """Test faculty can see their own submissions but not others'."""
        response = self.client.get(reverse("my_submissions"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Faculty 1 Project 1")
        self.assertContains(response, "Faculty 1 Project 2 Needs Revision")
        self.assertNotContains(response, "Faculty 2 Project")
        # Check if status is displayed
        self.assertContains(response, "Approved")
        self.assertContains(response, "Needs Revision")

    def test_my_submissions_view_unauthenticated(self):
        """Test unauthenticated users are redirected from my_submissions."""
        self.client.logout()
        response = self.client.get(reverse("my_submissions"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('my_submissions')}"
        )

    def test_edit_submission_get(self):
        """Test faculty can access edit form for their 'needs_revision' project."""
        response = self.client.get(reverse("edit_submission", args=[self.project2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Research Submission")
        self.assertContains(response, self.project2.title)
        # Check if revision reason is displayed
        self.assertContains(response, "Reason for revision request:")
        self.assertContains(response, "Please update abstract")

    def test_edit_submission_post_success(self):
        """Test faculty can successfully submit edits for their 'needs_revision' project."""
        edit_url = reverse("edit_submission", args=[self.project2.id])
        updated_data = {
            "title": "Faculty 1 Project 2 Updated",
            "abstract": "This is the updated abstract.",
            "student_author_name": self.project2.student_author_name,
            # Add other required fields from the form if necessary
        }
        # Simulate file data if form expects it (even if not changing)
        files_data = {}
        if self.project2.pdf_file:
            files_data["pdf_file"] = self.project2.pdf_file

        response = self.client.post(
            edit_url, updated_data, files=files_data, follow=True
        )

        self.assertRedirects(response, reverse("my_submissions"))
        self.assertContains(response, "Submission updated successfully")

        self.project2.refresh_from_db()
        self.assertEqual(self.project2.title, "Faculty 1 Project 2 Updated")
        self.assertEqual(self.project2.abstract, "This is the updated abstract.")
        self.assertEqual(self.project2.approval_status, "pending")  # Status resets

    def test_edit_submission_wrong_user(self):
        """Test faculty cannot edit another faculty's project."""
        self.client.logout()
        self.client.login(username="faculty2", password="password")
        response = self.client.get(reverse("edit_submission", args=[self.project2.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_edit_submission_not_needs_revision(self):
        """Test faculty cannot edit a project not in 'needs_revision' status."""
        response = self.client.get(
            reverse(
                "edit_submission", args=[self.project1.id]
            )  # Project 1 is 'approved'
        )
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_project_history_view(self):
        """Test faculty can view the history of their own project."""
        response = self.client.get(reverse("project_history", args=[self.project2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project History")
        self.assertContains(response, self.project2.title)
        self.assertContains(response, "pending")
        self.assertContains(response, "needs_revision")
        self.assertContains(response, "Please update abstract")

    def test_project_history_wrong_user(self):
        """Test faculty cannot view history of another faculty's project."""
        self.client.logout()
        self.client.login(username="faculty2", password="password")
        response = self.client.get(reverse("project_history", args=[self.project2.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden


class PublicViewsTest(TestCase):
    def setUp(self):
        self.faculty = User.objects.create_user(
            username="public_faculty", password="password", role="faculty"
        )
        self.approved_project = ResearchProject.objects.create(
            title="Approved Public Project",
            abstract="Public abstract",
            author=self.faculty,
            student_author_name="Public Student A",
            approval_status="approved",
        )
        self.pending_project = ResearchProject.objects.create(
            title="Pending Private Project",
            abstract="Private abstract",
            author=self.faculty,
            student_author_name="Private Student B",
            approval_status="pending",
        )
        self.client = Client()  # Anonymous client

    def test_project_detail_view_approved(self):
        """Test anonymous users can view details of an approved project."""
        response = self.client.get(
            reverse("project_detail", args=[self.approved_project.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Public Project")
        self.assertContains(response, "Public abstract")

    def test_project_detail_view_not_approved(self):
        """Test anonymous users cannot view details of a non-approved project."""
        response = self.client.get(
            reverse("project_detail", args=[self.pending_project.id])
        )
        self.assertEqual(response.status_code, 404)  # Should be Not Found


# --- Test from Step 2 of Implementation Guide ---
class ApproveResearchViewTest(TestCase):
    """Tests for the approve_research view with mock objects."""

    def setUp(self):
        # Create test users and project
        self.factory = RequestFactory()
        self.admin_user = User.objects.create_user(
            username="testadmin",
            email="admin@test.com",
            password="adminpass",
            role="admin",
        )
        self.faculty_user = User.objects.create_user(
            username="testfaculty",
            email="faculty@test.com",
            password="facultypass",
            role="faculty",
        )
        self.project = ResearchProject.objects.create(
            title="Test Project",
            abstract="Test abstract content that meets the minimum length requirement for validation purposes.",
            author=self.faculty_user,
            student_author_name="Test Student",
            approval_status="pending",
        )

    def _get_request_with_messages(self, url):
        """Helper to create a request with message middleware"""
        request = self.factory.get(url)
        request.user = self.admin_user
        # Add message middleware
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        return request

    @patch("research.views.send_status_change_email")
    @patch("research.views.create_in_app_notification")
    def test_approve_research_isolation(self, mock_notification, mock_email):
        """
        Test the approve_research view in isolation using mocks.

        This test verifies that:
        1. The view function updates the project status correctly
        2. It creates a status history record
        3. It sends an email notification (mocked)
        4. It creates an in-app notification (mocked)
        5. It redirects to the review page

        External dependencies (email sending and notifications) are mocked
        to isolate the view function's core logic.
        """
        # Create request with message middleware
        request = self._get_request_with_messages(
            reverse("approve_research", kwargs={"project_id": self.project.id})
        )

        # Call the view function directly
        response = approve_research(request, self.project.id)

        # Verify response status and redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("review_research"))

        # Verify database updates
        self.project.refresh_from_db()
        self.assertEqual(self.project.approval_status, "approved")

        # Verify history record was created
        history = StatusHistory.objects.filter(
            project=self.project, status_from="pending", status_to="approved"
        )
        self.assertTrue(history.exists())

        # Verify mocked functions were called appropriately
        mock_email.assert_called_once()
        mock_notification.assert_called_once()

        # Verify notification contained the right data
        notification_call = mock_notification.call_args
        self.assertEqual(
            notification_call[0][0], self.faculty_user
        )  # First arg: recipient
        self.assertIn(
            "approved", notification_call[0][1]
        )  # Second arg: message content
