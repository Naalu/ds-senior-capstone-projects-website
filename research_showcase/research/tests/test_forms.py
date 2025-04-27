from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..forms import (
    MAX_POSTER_SIZE_MB,
    MB_TO_BYTES,
    VALID_POSTER_EXTENSIONS,
    VALID_PRESENTATION_EXTENSIONS,
    ResearchProjectForm,
)

User = get_user_model()

# Constants for file size validation (assuming these are defined elsewhere)
# Need to ensure these match the values used in forms.py
MB_TO_BYTES = 1024 * 1024
MAX_POSTER_SIZE_MB = 5


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
        # Check for the error message from clean_poster_image
        expected_error = (
            f"Unsupported file extension. Use {', '.join(VALID_POSTER_EXTENSIONS)}"
        )
        self.assertIn(expected_error, form.errors["poster_image"])

    def test_form_invalid_poster_file_size(self):
        """Test form with poster file exceeding size limit."""
        # Create a valid but large image file (minimal content)
        large_content = b"a" * (MAX_POSTER_SIZE_MB * MB_TO_BYTES + 1)
        large_file = SimpleUploadedFile(
            "large.png", large_content, content_type="image/png"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(data=form_data, files={"poster_image": large_file})
        self.assertFalse(form.is_valid())
        self.assertIn("poster_image", form.errors)
        # Check for the error message from clean_poster_image
        expected_error = f"Image file too large (max {MAX_POSTER_SIZE_MB}MB)"
        self.assertIn(expected_error, form.errors["poster_image"])

    def test_form_invalid_presentation_file_type(self):
        """Test form with invalid file type for presentation."""
        invalid_file = SimpleUploadedFile(
            "test.txt", b"Not a presentation", content_type="text/plain"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(
            data=form_data, files={"presentation_file": invalid_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("presentation_file", form.errors)
        # Update expected error message to match form validation
        expected_error = f"Unsupported file extension. Use {', '.join(VALID_PRESENTATION_EXTENSIONS)}"
        self.assertIn(
            expected_error,
            form.errors["presentation_file"][0],
        )

    def test_form_invalid_presentation_file_size(self):
        """Test form with presentation file exceeding size limit."""
        large_content = b"a" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large.pdf", large_content, content_type="application/pdf"
        )
        form_data = self.base_valid_data.copy()
        form = ResearchProjectForm(
            data=form_data, files={"presentation_file": large_file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("presentation_file", form.errors)
        # This assertion comes from the custom clean_presentation_file method
        self.assertIn(
            "Presentation file too large", form.errors["presentation_file"][0]
        )

    def test_form_invalid_github_link(self):
        """Test form with invalid GitHub link."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = "not a valid url"
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("github_link", form.errors)
        self.assertIn("Enter a valid URL.", form.errors["github_link"][0])

    def test_form_valid_github_link_optional(self):
        """Test form is valid when GitHub link is omitted."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = ""
        form = ResearchProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_form_invalid_video_link(self):
        """Test form with invalid video link."""
        form_data = self.base_valid_data.copy()
        form_data["video_link"] = "not a valid url"
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("video_link", form.errors)
        self.assertIn("Enter a valid URL.", form.errors["video_link"][0])

    def test_form_valid_video_link_optional(self):
        """Test form is valid when video link is omitted."""
        form_data = self.base_valid_data.copy()
        form_data["video_link"] = ""
        form = ResearchProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_form_invalid_github_link_format_wrong_host(self):
        """Test clean_github_link rejects valid URL from wrong host."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = "https://gitlab.com/user/repo"
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("github_link", form.errors)
        self.assertIn(
            "Please enter a valid GitHub repository URL",
            form.errors["github_link"][0],
        )

    def test_form_invalid_github_link_format_incomplete(self):
        """Test clean_github_link rejects valid GitHub URL with missing repo path."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = "https://github.com/usernameonly"
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("github_link", form.errors)
        self.assertIn("GitHub URL should be in format:", form.errors["github_link"][0])

    def test_form_valid_github_link_format(self):
        """Test clean_github_link accepts a correctly formatted GitHub URL."""
        form_data = self.base_valid_data.copy()
        form_data["github_link"] = "https://github.com/username/repository"
        form = ResearchProjectForm(data=form_data)
        # Check if form is valid OR if github_link specifically has no errors
        if not form.is_valid():
            self.assertNotIn("github_link", form.errors)
        else:
            self.assertTrue(form.is_valid())

    def test_form_invalid_date_presented_future(self):
        """Test clean_date_presented rejects a date in the future."""
        future_date = date.today() + timedelta(days=1)
        form_data = self.base_valid_data.copy()
        form_data["date_presented"] = future_date.strftime(
            "%Y-%m-%d"
        )  # Format as string for form input
        form = ResearchProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("date_presented", form.errors)
        self.assertIn("cannot be in the future", form.errors["date_presented"][0])


class ResearchProjectFormValidationTest(TestCase):
    def setUp(self):
        # Basic valid data (adjust fields as necessary)
        self.valid_data = {
            "title": "Valid Title Length",
            "abstract": "This abstract is definitely long enough to meet the minimum length requirement.",
            "student_author_name": "Valid Student",
        }

    def test_poster_image_too_large(self):
        """Test validation fails if poster image file size exceeds the limit."""
        # Create a dummy file larger than the limit
        large_content = b"a" * (MAX_POSTER_SIZE_MB * MB_TO_BYTES + 1)
        # Use a valid extension that might pass initial checks if any remain
        large_file = SimpleUploadedFile(
            "large_poster.jpg", large_content, content_type="image/jpeg"
        )
        files_data = {"poster_image": large_file}

        form = ResearchProjectForm(data=self.valid_data, files=files_data)
        self.assertFalse(form.is_valid())
        self.assertIn("poster_image", form.errors)
        # Assert the error message from the clean_poster_image method
        self.assertIn(
            f"Image file too large (max {MAX_POSTER_SIZE_MB}MB)",
            form.errors["poster_image"],
        )

    def test_poster_image_invalid_extension(self):
        """Test validation fails if poster image file has an unsupported extension."""
        # Create a dummy file with an invalid extension (e.g., .txt)
        invalid_file = SimpleUploadedFile(
            "invalid_poster.txt", b"content", content_type="text/plain"
        )
        files_data = {"poster_image": invalid_file}

        form = ResearchProjectForm(data=self.valid_data, files=files_data)
        self.assertFalse(form.is_valid())
        self.assertIn("poster_image", form.errors)
        # Assert the error message from the clean_poster_image method
        # Need VALID_POSTER_EXTENSIONS imported or defined for the full message
        # from ..forms import VALID_POSTER_EXTENSIONS # <-- Add this import if needed
        expected_error_part = "Unsupported file extension."
        # Check if the specific error message is present in the list of errors for the field
        self.assertTrue(
            any(expected_error_part in error for error in form.errors["poster_image"])
        )
        # Optional: Assert the full message if VALID_POSTER_EXTENSIONS is available
        # expected_full_error = f"Unsupported file extension. Use {', '.join(VALID_POSTER_EXTENSIONS)}"
        # self.assertIn(expected_full_error, form.errors["poster_image"])

    # ... other validation tests will go here ...


# ... existing form tests if any ...
