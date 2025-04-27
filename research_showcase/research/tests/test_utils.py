from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import ResearchProject

User = get_user_model()


class SemesterUtilsTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testfaculty_utils",
            email="faculty_utils@example.com",
            password="testpassword123",
            role="faculty",
        )
        # Create test project
        self.project = ResearchProject.objects.create(
            title="Test Project For Utils",
            abstract="Abstract.",
            author=self.user,
            student_author_name="Util Student",
        )

    def test_year_presented_property(self):
        """Test the year_presented property (uses get_year_from_date utility)."""
        self.project.date_presented = date(2024, 5, 10)
        self.assertEqual(self.project.year_presented, 2024)
        self.project.date_presented = None
        self.project.save()  # Need to save for property to re-evaluate
        self.assertIsNone(self.project.year_presented)

    def test_semester_presented_property(self):
        """Test the semester_presented property (uses get_semester utility)."""
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
            self.project.save()  # Need to save for property to re-evaluate
            self.assertEqual(
                self.project.semester_presented,
                expected_semester,
                f"Failed for date {test_date}",
            )

        self.project.date_presented = None
        self.project.save()
        self.assertIsNone(self.project.semester_presented)
