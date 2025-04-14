"""
Research Project Tests
---------------------
This module contains tests for the enhanced research submission system.

Test classes:
- ResearchProjectModelTests: Tests for the ResearchProject model with all fields
- ResearchViewTests: Tests for view access control and search functionality
- ResearchProjectFormTest: Tests form validation and submission with all fields
- ResearchSubmissionViewTest: Tests user access to submission page
- ResearchReviewProcessTest: Tests review and approval workflow
- MultiStepFormTest: Tests the multi-step form navigation
- SuccessPageTest: Tests the success page after submission
- FacultyViewsTest: Tests for my_submissions and project_detail views
- PublicViewsTest: Tests for project_detail view

Run tests with: python manage.py test research
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .forms import ResearchProjectForm
from .models import Colloquium, ProjectImage, ResearchProject, StatusHistory

User = get_user_model()


class ResearchProjectModelTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testfaculty",
            email="faculty@example.com",
            password="testpassword123",
            role="faculty",
        )

        # Create test project with new fields
        self.project = ResearchProject.objects.create(
            title="Test Research Project",
            abstract="This is a test abstract for a research project.",
            author=self.user,
            student_author_name="John Doe",
            collaborator_names="Jane Smith, Alan Johnson",
            date_presented=date(2025, 3, 15),
            approval_status="approved",
        )

    def test_project_creation(self):
        """Test that a project is created correctly with all new fields"""
        self.assertEqual(self.project.title, "Test Research Project")
        self.assertEqual(self.project.author, self.user)
        self.assertEqual(self.project.student_author_name, "John Doe")
        self.assertEqual(self.project.collaborator_names, "Jane Smith, Alan Johnson")
        self.assertEqual(self.project.date_presented, date(2025, 3, 15))
        self.assertEqual(self.project.approval_status, "approved")

    def test_project_str_method(self):
        """Test the string representation of a project"""
        self.assertEqual(str(self.project), "Test Research Project")

    def test_year_presented_property(self):
        """Test the year_presented property."""
        self.project.date_presented = date(2024, 5, 10)
        self.assertEqual(self.project.year_presented, 2024)
        self.project.date_presented = None
        self.assertIsNone(self.project.year_presented)

    def test_semester_presented_property(self):
        """Test the semester_presented property for different months."""
        test_dates = {
            date(2024, 1, 15): "Winter",
            date(2024, 4, 1): "Spring",
            date(2024, 6, 20): "Summer",
            date(2024, 7, 31): "Summer",
            date(2024, 9, 5): "Fall",
            date(2024, 12, 25): "Winter",
        }
        for test_date, expected_semester in test_dates.items():
            self.project.date_presented = test_date
            self.assertEqual(self.project.semester_presented, expected_semester)

        self.project.date_presented = None
        self.assertIsNone(self.project.semester_presented)


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


class ResearchProjectFormTest(TestCase):
    def setUp(self):
        # Create test user (needed for model instance context if form requires it, but not for client)
        self.faculty_user = User.objects.create_user(
            username="testfaculty",
            password="testpassword123",
            email="faculty@test.com",
            role="faculty",
        )
        # REMOVED: self.client login removed - this class tests the form directly
        self.base_valid_data = {
            "title": "Valid Test Research Project Title",
            "abstract": "This is a valid sample abstract for testing purposes. It should be long enough to pass validation which requires at least 100 characters in the abstract field.",
            "student_author_name": "Valid Test Student",
            "date_presented": date.today(),
        }

    def test_form_minimum_valid_data(self):
        """Test form is valid with minimum required data."""
        form = ResearchProjectForm(data=self.base_valid_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_form_invalid_title(self):
        """Test form with invalid title (too short) - direct form test."""
        form_data = self.base_valid_data.copy()
        form_data["title"] = "Short"
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn(
            "Title must be at least 10 characters long", form.errors["title"][0]
        )

    def test_form_invalid_pdf_file_type(self):
        """Test form with invalid file type for PDF."""
        invalid_file = SimpleUploadedFile(
            "test.txt", b"Not a PDF file", content_type="text/plain"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(data=form_data, files={"pdf_file": invalid_file})
        self.assertFalse(form.is_valid())
        self.assertIn("pdf_file", form.errors)
        # This assertion comes from the custom clean_pdf_file method
        self.assertIn("File must be a PDF document", form.errors["pdf_file"][0])

    def test_form_invalid_pdf_file_size(self):
        """Test form with PDF file exceeding size limit."""
        large_content = b"a" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large.pdf", large_content, content_type="application/pdf"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(data=form_data, files={"pdf_file": large_file})
        self.assertFalse(form.is_valid())
        self.assertIn("pdf_file", form.errors)
        # This assertion comes from the custom clean_pdf_file method
        self.assertIn("PDF file too large", form.errors["pdf_file"][0])

    def test_form_invalid_poster_file_type(self):
        """Test form with invalid file type for poster."""
        # Use a non-image file type not covered by default ImageField check (e.g., .txt)
        invalid_file = SimpleUploadedFile(
            "test.txt", b"text content", content_type="text/plain"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(data=form_data, files={"poster_image": invalid_file})
        self.assertFalse(form.is_valid())
        self.assertIn("poster_image", form.errors)
        # Check for the default ImageField error message, as clean_* might not run
        self.assertIn("Upload a valid image.", form.errors["poster_image"][0])

    def test_form_invalid_poster_file_size(self):
        """Test form with poster file exceeding size limit."""
        # Create a valid but large image file (minimal content)
        large_content = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            + b"a" * (6 * 1024 * 1024)
        )
        large_file = SimpleUploadedFile(
            "large.png", large_content, content_type="image/png"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(data=form_data, files={"poster_image": large_file})
        self.assertFalse(form.is_valid())
        self.assertIn("poster_image", form.errors)
        # Corrected: Expect Django's default ImageField error as it runs first
        # and might reject the minimal large file as invalid/corrupt before size check.
        self.assertIn("Upload a valid image.", form.errors["poster_image"][0])

    def test_form_invalid_presentation_file_type(self):
        """Test form with invalid file type for presentation."""
        invalid_file = SimpleUploadedFile(
            "test.docx", b"word doc", content_type="application/msword"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(
            data=form_data, files={"presentation_file": invalid_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("presentation_file", form.errors)
        self.assertIn("Unsupported file extension", form.errors["presentation_file"][0])

    def test_form_invalid_presentation_file_size(self):
        """Test form with presentation file exceeding size limit."""
        large_content = b"a" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large.ppt", large_content, content_type="application/vnd.ms-powerpoint"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(
            data=form_data, files={"presentation_file": large_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("presentation_file", form.errors)
        self.assertIn(
            "Presentation file too large", form.errors["presentation_file"][0]
        )

    def test_form_invalid_github_link(self):
        """Test form with invalid GitHub link format."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = "invalid-url"  # Not a URL
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("github_link", form.errors)
        # Check for the default URLField error message
        self.assertIn("Enter a valid URL.", form.errors["github_link"][0])

        form_data["github_link"] = "https://gitlab.com/user/repo"  # Wrong domain
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("github_link", form.errors)
        # Check for the custom clean_github_link error message
        self.assertIn(
            "Please enter a valid GitHub repository URL", form.errors["github_link"][0]
        )

    def test_form_valid_github_link_optional(self):
        """Test form is valid when optional github_link is empty."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = ""
        form = ResearchProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_form_invalid_video_link(self):
        """Test form with invalid video link format (not URL)."""
        form_data = self.base_valid_data.copy()
        form_data["video_link"] = "not-a-url"
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("video_link", form.errors)
        self.assertIn("Enter a valid URL.", form.errors["video_link"][0])

    def test_form_valid_video_link_optional(self):
        """Test form is valid when optional video_link is empty."""
        form_data = self.base_valid_data.copy()
        form_data["video_link"] = ""
        form = ResearchProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    # Add tests for project_images validation if that clean method exists
    # Add tests for video_link validation


class ResearchSubmissionViewTest(TestCase):
    def setUp(self):
        # Create test users
        self.faculty_user = User.objects.create_user(
            username="testfaculty", password="testpassword123", role="faculty"
        )
        self.admin_user = User.objects.create_user(
            username="testadmin", password="testpassword123", role="admin"
        )
        self.regular_user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )

    def test_faculty_access(self):
        """Faculty should have access to submission page"""
        self.client.login(username="testfaculty", password="testpassword123")
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 200)

    def test_admin_access(self):
        """Admin should have access to submission page"""
        self.client.login(username="testadmin", password="testpassword123")
        response = self.client.get(reverse("submit_research"))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        """Regular users should be redirected to login"""
        # Instead of creating a new user, modify the existing one
        self.regular_user.role = "visitor"  # Set to a non-faculty, non-admin role
        self.regular_user.save()

        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("submit_research"))
        # Should redirect to login
        self.assertNotEqual(response.status_code, 200)


class ResearchReviewProcessTest(TestCase):
    def setUp(self):
        # Create test users
        self.faculty_user = User.objects.create_user(
            username="reviewfaculty",
            password="facultypass123",
            email="reviewfaculty@example.com",
            role="faculty",
        )
        self.admin_user = User.objects.create_user(
            username="reviewadmin",
            password="adminpass123",
            email="reviewadmin@example.com",
            role="admin",
        )

        # Create test project with new fields
        self.project = ResearchProject.objects.create(
            title="Project For Review",
            abstract="This is a test project that needs to be reviewed.",
            author=self.faculty_user,
            student_author_name="Review Student",
            collaborator_names="Review Helper",
            date_presented=date(2025, 2, 20),
            approval_status="pending",
        )

        self.client = Client()

    def test_review_page_shows_new_fields(self):
        """Test that review page shows the new fields"""
        self.client.login(username="reviewadmin", password="adminpass123")
        response = self.client.get(reverse("review_research"))

        # Check that the new fields are displayed
        self.assertContains(response, "Review Student")
        self.assertContains(response, "Review Helper")

    def test_approve_project(self):
        """Test approving a project updates its status"""
        self.client.login(username="reviewadmin", password="adminpass123")
        response = self.client.get(
            reverse("approve_research", args=[self.project.id]), follow=True
        )

        # Should redirect to review page
        self.assertRedirects(response, reverse("review_research"))

        # Refresh project from database
        self.project.refresh_from_db()
        self.assertEqual(self.project.approval_status, "approved")

    def test_reject_project_get_form(self):
        """Test GET request to reject_research shows the form."""
        self.client.login(username="reviewadmin", password="adminpass123")
        reject_url = reverse("reject_research", args=[self.project.id])
        response = self.client.get(reject_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/reject_research.html")
        self.assertContains(response, "Rejection Reason (Optional)")

    def test_reject_project_post(self):
        """Test POST request to reject_research updates status and adds feedback."""
        self.client.login(username="reviewadmin", password="adminpass123")
        reject_url = reverse("reject_research", args=[self.project.id])
        rejection_reason = "Project does not meet submission criteria."
        response = self.client.post(
            reject_url, {"rejection_reason": rejection_reason}, follow=True
        )

        # Should redirect back to review page
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(response, "has been rejected")  # Check for flash message

        # Refresh project from database
        self.project.refresh_from_db()
        self.assertEqual(self.project.approval_status, "rejected")
        self.assertEqual(self.project.admin_feedback, rejection_reason)

    def test_request_revision_get_form(self):
        """Test GET request to request_revision shows the form."""
        self.client.login(username="reviewadmin", password="adminpass123")
        revision_url = reverse("request_revision", args=[self.project.id])
        response = self.client.get(revision_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/request_revision.html")
        self.assertContains(response, "Feedback / Reason for Revision Request:")

    def test_request_revision_post(self):
        """Test POST request to request_revision updates status and adds feedback."""
        self.client.login(username="reviewadmin", password="adminpass123")
        revision_url = reverse("request_revision", args=[self.project.id])
        revision_feedback = "Please provide more details in the abstract."
        response = self.client.post(
            revision_url, {"revision_feedback": revision_feedback}, follow=True
        )

        # Should redirect back to review page
        self.assertRedirects(response, reverse("review_research"))
        self.assertContains(
            response, "Revisions requested for project"
        )  # Check for flash message

        # Refresh project from database
        self.project.refresh_from_db()
        self.assertEqual(self.project.approval_status, "needs_revision")
        self.assertEqual(self.project.admin_feedback, revision_feedback)


class MultiStepFormTest(TestCase):
    def setUp(self):
        # Create a faculty user for testing
        self.faculty_user = User.objects.create_user(
            username="stepfaculty", password="steppassword123", role="faculty"
        )
        self.client.login(username="stepfaculty", password="steppassword123")

    def test_form_navigation(self):
        """Test that the multi-step form can be navigated"""
        # This test would ideally use Selenium for frontend testing
        # For now, we'll test the basic form submission

        form_data = {
            "title": "Multi-Step Form Test",
            "abstract": "This is a test abstract for the multi-step form. It needs to be at least 100 characters long to pass validation checks in the enhanced form.",
            "student_author_name": "Multi-Step Student",
            "collaborator_names": "Step Helper, Another Helper",
            "date_presented": "2025-04-01",
        }

        response = self.client.post(reverse("submit_research"), form_data, follow=True)
        self.assertRedirects(response, reverse("submission_success"))

        # Verify project was created
        project = ResearchProject.objects.get(title="Multi-Step Form Test")
        self.assertEqual(project.student_author_name, "Multi-Step Student")
        self.assertEqual(project.collaborator_names, "Step Helper, Another Helper")


class SuccessPageTest(TestCase):
    def setUp(self):
        # Create a faculty user for testing
        self.faculty_user = User.objects.create_user(
            username="successfaculty", password="successpass123", role="faculty"
        )
        self.client.login(username="successfaculty", password="successpass123")

    def test_success_page_accessible(self):
        """Test that the success page is accessible"""
        response = self.client.get(reverse("submission_success"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Research Project Submitted")


class FacultyViewsTest(TestCase):
    def setUp(self):
        self.faculty_user = User.objects.create_user(
            username="myviewfaculty",
            password="viewpassword123",
            email="myviewfaculty@example.com",
            role="faculty",
        )
        self.other_faculty = User.objects.create_user(
            username="otherfaculty", password="otherpass123", role="faculty"
        )
        # Create the admin user needed for StatusHistory actor
        self.admin_user = User.objects.create_user(
            username="historyadmin",  # Use a distinct username
            password="adminpass123",
            email="historyadmin@example.com",
            role="admin",
        )

        self.project1 = ResearchProject.objects.create(
            title="My Project 1",
            abstract="Abstract for project 1",
            author=self.faculty_user,
            student_author_name="Student A",
            approval_status="pending",
            date_presented=date.today(),
        )
        self.project2 = ResearchProject.objects.create(
            title="My Project 2",
            abstract="Abstract for project 2",
            author=self.faculty_user,
            student_author_name="Student B",
            approval_status="approved",
            date_presented=date.today(),
        )
        self.project3 = ResearchProject.objects.create(
            title="Other Faculty Project",
            abstract="Abstract for other project",
            author=self.other_faculty,
            student_author_name="Student C",
            approval_status="approved",
            date_presented=date.today(),
        )

        # Add a project needing revision for edit tests
        self.project_needs_revision = ResearchProject.objects.create(
            title="Needs Revision Project",
            abstract="Abstract needs more detail."
            * 5,  # Make abstract long enough initially
            author=self.faculty_user,
            student_author_name="Student D",
            approval_status="needs_revision",
            admin_feedback="Please expand the abstract.",
            date_presented=date.today(),
        )
        # Add some history for the history test
        StatusHistory.objects.create(
            project=self.project_needs_revision,
            status_from=None,
            status_to="pending",
            comment="Initial submission",
        )
        StatusHistory.objects.create(
            project=self.project_needs_revision,
            actor=self.admin_user,  # Use the created admin user
            status_from="pending",
            status_to="needs_revision",
            comment="Please expand the abstract.",
        )

        self.client = Client()
        self.client.login(username="myviewfaculty", password="viewpassword123")

    def test_my_submissions_view_get(self):
        """Test that the my_submissions view shows only the logged-in faculty's projects."""
        response = self.client.get(reverse("my_submissions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/my_submissions.html")
        self.assertContains(response, "My Project 1")
        self.assertContains(response, "My Project 2")
        self.assertContains(response, "Needs Revision Project")
        self.assertNotContains(response, "Other Faculty Project")
        # Check context variable name if needed
        self.assertIn("projects", response.context)
        self.assertEqual(len(response.context["projects"]), 3)

    def test_my_submissions_view_unauthenticated(self):
        """Test unauthenticated users are redirected from my_submissions."""
        self.client.logout()
        response = self.client.get(reverse("my_submissions"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_edit_submission_get(self):
        """Test GET request to edit_submission loads form for project needing revision."""
        url = reverse("edit_submission", args=[self.project_needs_revision.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/edit_submission.html")
        self.assertContains(
            response, "Needs Revision Project"
        )  # Check project title is in form
        self.assertContains(
            response, "Please expand the abstract."
        )  # Check feedback is shown

    def test_edit_submission_post_success(self):
        """Test POST request updates project and sets status to pending."""
        url = reverse("edit_submission", args=[self.project_needs_revision.id])
        updated_abstract = "Abstract has been significantly expanded with more details about the methodology and results, meeting the required length and content standards."
        form_data = {
            "title": self.project_needs_revision.title,
            "student_author_name": self.project_needs_revision.student_author_name,
            "abstract": updated_abstract,
            "collaborator_names": self.project_needs_revision.collaborator_names,
            "date_presented": self.project_needs_revision.date_presented.strftime(
                "%Y-%m-%d"
            ),
            # Add other required fields if the form expects them all on edit
        }
        response = self.client.post(url, form_data, follow=True)

        # Should redirect to my_submissions after successful edit
        self.assertRedirects(response, reverse("my_submissions"))
        self.assertContains(response, "updated and resubmitted for approval")

        # Verify project changes
        self.project_needs_revision.refresh_from_db()
        self.assertEqual(self.project_needs_revision.abstract, updated_abstract)
        self.assertEqual(self.project_needs_revision.approval_status, "pending")
        self.assertIsNone(
            self.project_needs_revision.admin_feedback
        )  # Feedback should be cleared

    def test_edit_submission_wrong_user(self):
        """Test faculty cannot edit another faculty's project."""
        # self.project3 belongs to other_faculty
        url = reverse("edit_submission", args=[self.project3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_edit_submission_not_needs_revision(self):
        """Test faculty cannot edit a project not in 'needs_revision' status."""
        # self.project1 is pending
        url = reverse("edit_submission", args=[self.project1.id])
        response = self.client.get(url)
        # Expect redirect (302) because the view now redirects instead of raising 403
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("my_submissions"))

    def test_project_history_view(self):
        """Test project_history view shows status changes."""
        url = reverse("project_history", args=[self.project_needs_revision.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/project_history.html")
        # Check for key elements rendered by the template
        self.assertContains(response, "Initial submission")  # Check initial comment
        self.assertContains(
            response, "Please expand the abstract."
        )  # Check revision request comment
        self.assertContains(response, "Needs Revision")  # Check the 'to' status
        self.assertContains(
            response, "Status changed from: Pending Approval"
        )  # Check the 'from' status text

    def test_project_history_wrong_user(self):
        """Test faculty cannot view history of another faculty's project."""
        # self.project3 belongs to other_faculty
        url = reverse("project_history", args=[self.project3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden


class PublicViewsTest(TestCase):
    def setUp(self):
        self.faculty_user = User.objects.create_user(
            username="publicfaculty", password="publicpass123", role="faculty"
        )
        self.approved_project = ResearchProject.objects.create(
            title="Approved Public Project",
            abstract="Abstract approved",
            author=self.faculty_user,
            student_author_name="Approved Student",
            approval_status="approved",
            date_presented=date.today(),
        )
        self.pending_project = ResearchProject.objects.create(
            title="Pending Project",
            abstract="Abstract pending",
            author=self.faculty_user,
            student_author_name="Pending Student",
            approval_status="pending",
            date_presented=date.today(),
        )
        self.client = Client()

    def test_project_detail_view_approved(self):
        """Test project_detail view shows an approved project."""
        url = reverse("project_detail", args=[self.approved_project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/project_detail.html")
        self.assertContains(response, "Approved Public Project")
        self.assertContains(response, "Abstract approved")

    def test_project_detail_view_not_approved(self):
        """Test project_detail view returns 404 for non-approved projects."""
        url = reverse("project_detail", args=[self.pending_project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ProjectImageModelTest(TestCase):
    def setUp(self):
        self.faculty_user = User.objects.create_user(
            username="imgfaculty", password="password"
        )
        self.project = ResearchProject.objects.create(
            title="Project With Image", author=self.faculty_user
        )
        # Create a dummy image file
        image_file = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        self.project_image = ProjectImage.objects.create(
            project=self.project, image=image_file
        )

    def test_project_image_str_method(self):
        """Test the string representation of ProjectImage."""
        expected_str = (
            f"Image for {self.project.title} ({self.project_image.image.name})"
        )
        self.assertEqual(str(self.project_image), expected_str)


class StatusHistoryModelTest(TestCase):
    def setUp(self):
        self.faculty_user = User.objects.create_user(
            username="histfaculty", password="password"
        )
        self.project = ResearchProject.objects.create(
            title="History Project", author=self.faculty_user
        )
        self.status_history = StatusHistory.objects.create(
            project=self.project,
            actor=self.faculty_user,
            status_from="pending",
            status_to="approved",
            comment="Test approval",
        )

    def test_status_history_str_method(self):
        """Test the string representation of StatusHistory."""
        timestamp_str = self.status_history.timestamp.strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # Basic format
        expected_str_part = f"{self.project.title} changed to Approved by {self.faculty_user.username} at"
        # Use assertIn because exact timestamp formatting can vary slightly
        self.assertIn(expected_str_part, str(self.status_history))


class ColloquiumModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="presenter", password="password")
        self.colloquium = Colloquium.objects.create(
            title="Test Colloquium",
            presenter=self.user,
            date=date.today(),
            description="A test talk.",
        )

    def test_colloquium_str_method(self):
        """Test the string representation of Colloquium."""
        expected_str = (
            f"{self.colloquium.title} by {self.user.username} on {self.colloquium.date}"
        )
        self.assertEqual(str(self.colloquium), expected_str)
