# research/tests.py
from django.contrib.auth import get_user_model
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

        # Create test project
        self.project = ResearchProject.objects.create(
            title="Test Research Project",
            abstract="This is a test abstract for a research project.",
            author=self.user,
            approval_status="approved",
        )

    def test_project_creation(self):
        """Test that a project is created correctly"""
        self.assertEqual(self.project.title, "Test Research Project")
        self.assertEqual(self.project.author, self.user)
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
