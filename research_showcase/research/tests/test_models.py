from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Colloquium, ProjectImage, ResearchProject, StatusHistory

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

    # NOTE: test_year_presented_property and test_semester_presented_property
    # moved to test_utils.py as they test utility functions


class ProjectImageModelTest(TestCase):
    def setUp(self):
        # Create test user
        faculty_user = User.objects.create_user(
            username="testfaculty_img",
            email="faculty_img@example.com",
            password="testpassword123",
            role="faculty",
        )
        # Create a project to associate the image with
        self.project = ResearchProject.objects.create(
            title="Project For Image",
            abstract="Abstract for image project",
            author=faculty_user,
            student_author_name="Image Student",
            approval_status="approved",
        )
        # Create a ProjectImage instance
        self.project_image = ProjectImage.objects.create(
            project=self.project, caption="Test Image Caption"
        )

    def test_project_image_str_method(self):
        """Test the string representation of a project image."""
        expected_str = f"Image for {self.project.title}: Test Image Caption"
        self.assertEqual(str(self.project_image), expected_str)


class StatusHistoryModelTest(TestCase):
    def setUp(self):
        # Create test users
        faculty_user = User.objects.create_user(
            username="testfaculty_hist", password="password", role="faculty"
        )
        self.admin_user = User.objects.create_user(
            username="testadmin_hist", password="password", role="admin"
        )
        # Create a project
        self.project = ResearchProject.objects.create(
            title="History Test Project",
            abstract="Test abstract.",
            author=faculty_user,
            student_author_name="History Student",
        )
        # Create a status history entry
        self.history_entry = StatusHistory.objects.create(
            project=self.project,
            status_from="pending",
            status_to="approved",
            changed_by=self.admin_user,
            comment="Initial approval.",
        )

    def test_status_history_str_method(self):
        """Test the string representation of a status history record."""
        expected_str = f"{self.project.title} changed from pending to approved by {self.admin_user.username}"
        self.assertEqual(str(self.history_entry), expected_str)


class ColloquiumModelTest(TestCase):
    def setUp(self):
        # Create a Colloquium instance
        self.colloquium = Colloquium.objects.create(
            semester="Fall", year=2024, date=date(2024, 10, 15)
        )

    def test_colloquium_str_method(self):
        """Test the string representation of a colloquium."""
        self.assertEqual(str(self.colloquium), "Fall 2024 Colloquium")
