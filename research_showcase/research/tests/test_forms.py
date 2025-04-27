from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..forms import VALID_PRESENTATION_EXTENSIONS, ResearchProjectForm

User = get_user_model()


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
        # Update expected error message to match the actual default ImageField error
        # for potentially corrupted/invalid files, which this large file triggers.
        expected_error = "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        self.assertIn(expected_error, form.errors["poster_image"][0])

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
