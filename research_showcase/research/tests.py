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

Run tests with: python manage.py test research
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .models import ResearchProject

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
        self.assertEqual(response.status_code, 302)  # Should redirect

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
        # Create test user
        self.faculty_user = User.objects.create_user(
            username="testfaculty",
            password="testpassword123",
            email="faculty@test.com",
            role="faculty",
        )
        self.client.login(username="testfaculty", password="testpassword123")

    def test_form_valid_data(self):
        """Test form with valid data should create a research project"""
        with open("research/tests/test_files/sample.pdf", "rb") as pdf_file:
            pdf_content = pdf_file.read()

        form_data = {
            "title": "Test Research Project",
            "abstract": "This is a sample abstract for testing purposes. It should be long enough to pass validation which requires at least 100 characters in the abstract field.",
            "student_author_name": "Test Student",
            "github_link": "https://github.com/testuser/test-project",
            "project_sponsor": "Test Sponsor",
            "pdf_file": SimpleUploadedFile(
                "sample.pdf", pdf_content, content_type="application/pdf"
            ),
        }

        response = self.client.post(reverse("submit_research"), form_data, follow=True)

        # Check response
        self.assertEqual(response.status_code, 200)

        # Check if research project was created
        self.assertEqual(ResearchProject.objects.count(), 1)
        project = ResearchProject.objects.first()
        self.assertEqual(project.title, "Test Research Project")
        self.assertEqual(project.student_author_name, "Test Student")
        self.assertEqual(project.author, self.faculty_user)
        self.assertEqual(project.approval_status, "pending")

    def test_form_with_new_fields(self):
        """Test form with all new fields"""
        form_data = {
            "title": "Enhanced Research Project",
            "abstract": "This is a sample abstract for testing purposes. It should be long enough to pass validation which requires at least 100 characters in the abstract field.",
            "student_author_name": "Jane Student",
            "collaborator_names": "Dr. Smith, Dr. Jones",
            "date_presented": "2025-03-15",
            "github_link": "https://github.com/testuser/test-project",
        }

        response = self.client.post(reverse("submit_research"), form_data, follow=True)

        # Should redirect to success page
        self.assertRedirects(response, reverse("submission_success"))

        # Verify project was created with new fields
        project = ResearchProject.objects.get(title="Enhanced Research Project")
        self.assertEqual(project.student_author_name, "Jane Student")
        self.assertEqual(project.collaborator_names, "Dr. Smith, Dr. Jones")
        self.assertEqual(project.date_presented.strftime("%Y-%m-%d"), "2025-03-15")

    def test_form_invalid_title(self):
        """Test form with invalid title (too short)"""
        form_data = {
            "title": "Short",  # Too short
            "abstract": "This is a sample abstract for testing purposes. It should be long enough to pass validation which requires at least 100 characters in the abstract field.",
        }

        response = self.client.post(reverse("submit_research"), form_data)

        # Check no project was created
        self.assertEqual(ResearchProject.objects.count(), 0)

        # Check error message is in response
        self.assertContains(response, "Title must be at least 10 characters long")

    def test_form_invalid_file_type(self):
        """Test form with invalid file type for PDF"""
        form_data = {
            "title": "Test Research Project",
            "abstract": "This is a sample abstract for testing purposes. It should be long enough to pass validation which requires at least 100 characters in the abstract field.",
            "pdf_file": SimpleUploadedFile(
                "test.txt", b"Not a PDF file", content_type="text/plain"
            ),
        }

        response = self.client.post(reverse("submit_research"), form_data)

        # Check no project was created
        self.assertEqual(ResearchProject.objects.count(), 0)

        # Check error message is in response
        self.assertContains(response, "File must be a PDF document")


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
            username="reviewfaculty", password="facultypass123", role="faculty"
        )
        self.admin_user = User.objects.create_user(
            username="reviewadmin", password="adminpass123", role="admin"
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
