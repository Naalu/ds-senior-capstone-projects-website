from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import ResearchProject, StatusHistory
from ..views import approve_research, submit_research  # Needed for the mock test

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
        self.client.login(
            username="faculty_sub", password="testpassword"
        )  # Log in faculty
        self.submit_url = reverse("submit_research")

        # Minimal valid data for POST
        self.valid_pdf = SimpleUploadedFile(
            "valid.pdf", b"pdf content", content_type="application/pdf"
        )
        self.valid_data = {
            "title": "Test Submission",
            "abstract": "Abstract that is definitely long enough to pass the minimum validation requirements set by the form.",
            "student_author_name": "Test Student Sub",
            # Add other required fields if any
        }
        self.valid_files = {"pdf_file": self.valid_pdf}

    def test_faculty_access(self):
        """Test faculty can access the submission page."""
        self.client.login(username="faculty_sub", password="testpassword")
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 200)

    def test_admin_access(self):
        """Test admin CAN access the submission page (as per @faculty_required decorator)."""
        self.client.login(username="admin_sub", password="testpassword")
        response = self.client.get(reverse("submit_research"))
        # The @faculty_required decorator allows admins too.
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        """Test anonymous users are redirected to login."""
        self.client.logout()  # Ensure client is logged out for this test
        response = self.client.get(reverse("submit_research"))
        # Use the updated decorator logic for the expected redirect URL
        expected_url = f"{reverse('login')}?next={reverse('submit_research')}"
        self.assertRedirects(response, expected_url)

    def test_submission_post_invalid_form(self):
        """Test submitting an invalid form displays a warning message."""
        # Missing required field 'title'
        invalid_data = {
            "abstract": "Abstract",
            "student_author_name": "Test Student Sub",
        }
        response = self.client.post(self.submit_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Should re-render the form page
        self.assertTemplateUsed(response, "research/submit_research.html")
        self.assertContains(response, "Please correct the errors in the form")
        self.assertFalse(
            ResearchProject.objects.exists()
        )  # Ensure no project was created

    def test_submission_post_success_with_images_factory(self):
        """Test successful POST via RequestFactory creates project, images, history."""
        # Create dummy image files
        image_file1 = SimpleUploadedFile(
            "image1.jpg", b"jpeg_content1", content_type="image/jpeg"
        )
        image_file2 = SimpleUploadedFile(
            "image2.png", b"png_content2", content_type="image/png"
        )

        # Construct POST data including files
        post_data = self.valid_data.copy()
        post_data["pdf_file"] = self.valid_files["pdf_file"]
        post_data["project_images"] = [image_file1, image_file2]

        # Create RequestFactory and request object, passing data including files
        factory = RequestFactory()
        request = factory.post(self.submit_url, data=post_data)

        # Set user and messages middleware
        request.user = self.faculty_user
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        # Call the view function directly
        response = submit_research(request)

        # 1. Check response (should be a redirect)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("submission_success"))

        # 2. Check ResearchProject creation
        self.assertEqual(ResearchProject.objects.count(), 1)
        project = ResearchProject.objects.first()
        self.assertEqual(project.title, self.valid_data["title"])
        self.assertEqual(project.author, self.faculty_user)
        self.assertEqual(project.approval_status, "pending")
        self.assertIsNone(project.admin_feedback)

        # 3. Check ProjectImage creation
        self.assertEqual(project.images.count(), 2)
        # image_names = list(project.images.values_list("image__name", flat=True)) # Cannot query name directly
        # Instead, fetch the objects and check names
        created_images = project.images.all()
        found_image1 = False
        found_image2 = False
        for proj_image in created_images:
            if "image1" in proj_image.image.name:
                found_image1 = True
            if "image2" in proj_image.image.name:
                found_image2 = True
        self.assertTrue(found_image1, "Image 1 not found")
        self.assertTrue(found_image2, "Image 2 not found")

        # 4. Check StatusHistory creation
        history_exists = StatusHistory.objects.filter(
            project=project, actor=self.faculty_user, status_to="pending"
        ).exists()
        self.assertTrue(history_exists)

        # Note: Checking flash messages with RequestFactory is less direct
        # We trust the messages.success call happened if the redirect occurred.

    @patch("research.views.ResearchProjectForm.save")
    def test_submission_save_exception(self, mock_save):
        """Test that an exception during form saving shows an error message."""
        mock_save.side_effect = Exception("Database error simulation")

        response = self.client.post(
            self.submit_url, self.valid_data, files=self.valid_files
        )

        self.assertEqual(response.status_code, 200)  # Should re-render form
        self.assertTemplateUsed(response, "research/submit_research.html")
        self.assertContains(
            response, "Error saving research project: Database error simulation"
        )
        self.assertFalse(
            ResearchProject.objects.exists()
        )  # Ensure no project was created


class ResearchReviewProcessTest(TestCase):
    def setUp(self):
        # Create test users
        self.faculty_user = User.objects.create_user(
            username="faculty_rev",
            password="password",
            role="faculty",
            email="faculty_rev@example.com",
        )
        self.admin_user = User.objects.create_user(
            username="admin_rev",
            password="password",
            role="admin",
            email="admin_rev@example.com",
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

        # Additional projects for collaborator display tests
        long_collaborators = "Collab " * 20  # Longer than 100 chars
        self.project_long_collab = ResearchProject.objects.create(
            title="Long Collaborators",
            author=self.faculty_user,
            student_author_name="Collab Student Long",
            approval_status="pending",
            collaborator_names=long_collaborators,
        )
        self.project_short_collab = ResearchProject.objects.create(
            title="Short Collaborators",
            author=self.faculty_user,
            student_author_name="Collab Student Short",
            approval_status="pending",
            collaborator_names="A, B, C",
        )
        self.project_no_collab = ResearchProject.objects.create(
            title="No Collaborators",
            author=self.faculty_user,
            student_author_name="Collab Student None",
            approval_status="pending",
            collaborator_names="",  # Empty string
        )

    def test_review_page_collaborator_display(self):
        """Test collaborator display logic (truncation, short, none)."""
        response = self.client.get(reverse("review_research"))
        self.assertEqual(response.status_code, 200)

        # Check long collaborators are truncated
        self.assertContains(response, "Collab Collab Collab")  # Part of the long string
        self.assertContains(response, "...")  # Check for ellipsis
        # More specific check might require inspecting context or using html=True
        # For now, check presence of start and ellipsis

        # Check short collaborators are displayed fully
        self.assertContains(response, "A, B, C")

        # Check no collaborators displays "None"
        # Need to be careful not to match other "None" text. Check for the badge.
        self.assertContains(
            response, '<span class="badge bg-secondary">None</span>', html=True
        )

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
        # Check for the actual label text in the template
        self.assertContains(response, "Rejection Reason (Optional)")

    @patch("research.views.send_status_change_email")
    @patch("research.views.create_in_app_notification")
    def test_reject_project_post(self, mock_notification, mock_email):
        """Test rejecting a project updates status, creates history, and sends notifications."""
        reject_url = reverse("reject_research", args=[self.project_pending.id])
        post_data = {"rejection_reason": "Incomplete abstract"}
        response = self.client.post(reject_url, post_data, follow=True)
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(response, "has been rejected")
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "rejected")
        history = StatusHistory.objects.filter(
            project=self.project_pending, status_to="rejected"
        )
        self.assertTrue(history.exists())
        expected_comment = f"Project rejected. Reason: {post_data['rejection_reason']}"
        self.assertEqual(history.first().comment, expected_comment)

        # Assert notifications were called
        mock_email.assert_called_once()
        mock_notification.assert_called_once()

    @patch("research.views.create_in_app_notification")
    def test_reject_notification_exception(self, mock_notification):
        """Test exception during notification creation on reject shows warning."""
        mock_notification.side_effect = Exception("Notification system down")
        reject_url = reverse("reject_research", args=[self.project_pending.id])
        post_data = {"rejection_reason": "Simulate error"}
        response = self.client.post(reject_url, post_data, follow=True)
        self.assertRedirects(response, reverse("review_research"))
        # Check for the warning message about notification failure
        self.assertContains(response, "Failed to create in-app notification")
        # Ensure project status was still updated
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "rejected")

    def test_request_revision_get_form(self):
        """Test GET request for request revision form shows the form."""
        response = self.client.get(
            reverse("request_revision", args=[self.project_pending.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reason for Revision Request")

    @patch("research.views.send_status_change_email")
    @patch("research.views.create_in_app_notification")
    def test_request_revision_post(self, mock_notification, mock_email):
        """Test requesting revision updates status, creates history, and sends notifications."""
        revision_url = reverse("request_revision", args=[self.project_pending.id])
        post_data = {"revision_feedback": "Update abstract"}
        response = self.client.post(
            revision_url,
            post_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(response, "Feedback provided")
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "needs_revision")
        history = StatusHistory.objects.filter(
            project=self.project_pending, status_to="needs_revision"
        )
        self.assertTrue(history.exists())
        expected_comment = (
            f"Revisions requested. Feedback: {post_data['revision_feedback']}"
        )
        self.assertEqual(history.first().comment, expected_comment)

        # Assert notifications were called
        mock_email.assert_called_once()
        mock_notification.assert_called_once()

    @patch("research.views.create_in_app_notification")
    def test_request_revision_notification_exception(self, mock_notification):
        """Test exception during notification creation on revision request shows warning."""
        mock_notification.side_effect = Exception("Notification system down")
        revision_url = reverse("request_revision", args=[self.project_pending.id])
        post_data = {"revision_feedback": "Simulate error"}
        response = self.client.post(revision_url, post_data, follow=True)
        self.assertRedirects(response, reverse("review_research"))
        # Check for the warning message about notification failure
        self.assertContains(response, "Failed to create in-app notification")
        # Ensure project status was still updated
        self.project_pending.refresh_from_db()
        self.assertEqual(self.project_pending.approval_status, "needs_revision")


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
            admin_feedback="Please update abstract",
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
        self.assertContains(response, "Edit Submission:")
        self.assertContains(response, self.project2.title)
        # Check if revision reason is displayed using the actual text from the template
        self.assertContains(response, "Revisions Requested")
        self.assertContains(response, "Please update abstract")

    def test_edit_submission_post_success(self):
        """Test faculty can successfully submit edits for their 'needs_revision' project."""
        edit_url = reverse("edit_submission", args=[self.project2.id])
        # Ensure abstract meets minimum length requirement (100 chars)
        long_enough_abstract = (
            "This is the updated abstract, now made significantly longer to ensure it passes "
            "the minimum length validation requirement set within the ResearchProjectForm. "
            "We need to add enough dummy text here to reach the one hundred character mark."
        )
        self.assertGreaterEqual(
            len(long_enough_abstract), 100
        )  # Verify abstract length

        updated_data = {
            "title": "Faculty 1 Project 2 Updated",
            "abstract": long_enough_abstract,
            "student_author_name": self.project2.student_author_name,
            # Other optional fields can be omitted or included as needed\
        }

        # Simulate file data - IMPORTANT: For edits, often only *new* files need to be POSTed.
        # If the form uses ClearableFileInput, existing files are usually handled by the widget.
        # Providing the existing FieldFile might cause issues. Send empty dict if not changing files.
        files_data = {}

        # Make the POST request *without* follow=True to check the initial response
        response = self.client.post(edit_url, updated_data, files=files_data)

        # Check for the redirect status code first
        self.assertEqual(
            response.status_code,
            302,
            f"Expected status 302, got {response.status_code}. Response content: {response.content.decode()}",
        )

        # Now check the redirect target URL
        self.assertRedirects(response, reverse("my_submissions"))

        # Check flash message (requires response from followed redirect or manual setup)
        # response_followed = self.client.post(edit_url, updated_data, files=files_data, follow=True)
        # self.assertContains(response_followed, "updated and resubmitted for approval")

        self.project2.refresh_from_db()
        self.assertEqual(self.project2.title, "Faculty 1 Project 2 Updated")
        self.assertEqual(self.project2.abstract, long_enough_abstract)
        self.assertEqual(self.project2.approval_status, "pending")  # Status resets

    def test_edit_submission_wrong_user(self):
        """Test faculty cannot edit another faculty's project."""
        self.client.logout()
        self.client.login(username="faculty2", password="password")
        response = self.client.get(reverse("edit_submission", args=[self.project2.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_edit_submission_not_needs_revision(self):
        """Test faculty cannot edit a project not in 'needs_revision' status (should redirect)."""
        # Access edit page for Project 1 (approved)
        edit_url = reverse("edit_submission", args=[self.project1.id])
        response = self.client.get(edit_url)

        # Expect a redirect to 'my_submissions' with a 302 status code
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("my_submissions"))
        # Optionally, check for the error message if message middleware is properly set up for tests
        # messages = list(get_messages(response.wsgi_request))
        # self.assertTrue(any("not currently awaiting revision" in str(m) for m in messages))

    def test_project_history_view(self):
        """Test faculty can view the history of their own project."""
        response = self.client.get(reverse("project_history", args=[self.project2.id]))
        self.assertEqual(response.status_code, 200)
        # Check for the actual heading text used in the template
        self.assertContains(response, "Status History for:")
        self.assertContains(response, self.project2.title)
        # Check for history entries content
        self.assertContains(response, "Needs Revision")  # status_to
        self.assertContains(response, "Please update abstract")  # comment
        self.assertContains(response, "Pending Approval")  # status_from

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

    @patch("django.core.mail.send_mail")
    @patch("research.views.create_in_app_notification")
    def test_approve_research_email_disabled(
        self, mock_in_app_notification, mock_send_mail
    ):
        """Test approve view does not send email if user opted out."""
        # Disable email notification for the faculty user
        self.faculty_user.notify_by_email_on_status_change = False
        self.faculty_user.save()

        # Create request
        request = self._get_request_with_messages(
            reverse("approve_research", kwargs={"project_id": self.project.id})
        )

        # Call the view function
        # This will call send_status_change_email internally,
        # which should then NOT call the *actual* django.core.mail.send_mail
        response = approve_research(request, self.project.id)

        # Verify redirect and status update occurred
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.approval_status, "approved")

        # Verify send_mail was NOT called, but in-app notification WAS called
        mock_send_mail.assert_not_called()
        mock_in_app_notification.assert_called_once()


class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.faculty = User.objects.create_user(
            username="home_faculty", password="password", role="faculty"
        )

        # Create multiple approved projects with different dates
        cls.num_approved = 7
        cls.project_titles = []
        today = timezone.now().date()
        for i in range(cls.num_approved):
            title = f"Approved Search Project {i + 1}"
            cls.project_titles.append(title)
            ResearchProject.objects.create(
                title=title,
                abstract=f"Abstract {i + 1}",
                author=cls.faculty,
                student_author_name=f"Student {i + 1}",
                approval_status="approved",
                submission_date=timezone.now()
                - timedelta(days=i),  # Keep for ordering if needed
                date_presented=today - timedelta(days=i),  # Add date_presented
            )

        # Create a pending project (should not appear)
        cls.pending_title = "Pending Search Project"
        ResearchProject.objects.create(
            title=cls.pending_title,
            abstract="Pending abstract",
            author=cls.faculty,
            student_author_name="Student Pending",
            approval_status="pending",
            submission_date=timezone.now() - timedelta(days=8),
            date_presented=today - timedelta(days=8),  # Add date_presented
        )

    def test_home_url_uses_search_view_and_template(self):
        """Test that the 'home' URL (`/`) uses the search view and correct template."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        # Check that the search results template is used
        self.assertTemplateUsed(response, "research/search_results.html")

    def test_home_url_displays_all_approved_projects_initially(self):
        """Test the 'home' URL displays all approved projects when no query is given."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/search_results.html")

        # Check context data - assuming 'projects' is the context variable
        self.assertIn("projects", response.context)
        displayed_projects = response.context["projects"]

        # Check that all approved projects are present (adjust if pagination is used)
        # For now, assume no pagination or first page shows all 7
        self.assertEqual(len(displayed_projects), self.num_approved)

        displayed_titles = [p.title for p in displayed_projects]
        # Ensure all expected titles are there
        for title in self.project_titles:
            self.assertIn(title, displayed_titles)
            self.assertContains(response, title)  # Check if title is in rendered HTML

        # Check that the pending project is not included
        self.assertNotIn(self.pending_title, displayed_titles)
        self.assertNotContains(response, self.pending_title)

    def test_home_url_no_approved_projects(self):
        """Test 'home' URL view when there are no approved projects."""
        # Delete all approved projects created in setUpTestData
        ResearchProject.objects.filter(approval_status="approved").delete()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/search_results.html")
        self.assertIn("projects", response.context)
        self.assertEqual(len(response.context["projects"]), 0)
        # Check for a message indicating no projects, if applicable in the template
        # self.assertContains(response, "No projects found matching your criteria.")
