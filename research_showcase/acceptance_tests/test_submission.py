import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .pages.login_page import LoginPage  # Use relative import
from .pages.submission_page import SubmissionPage  # Use relative import


@pytest.mark.django_db  # Mark test to use the database
@pytest.mark.acceptance  # Custom marker for acceptance tests
class TestResearchSubmission:
    """
    Acceptance tests for the research submission workflow.

    These tests verify the multi-step form process from faculty login
    through project submission and confirmation.
    """

    @pytest.fixture(autouse=True)
    def setup_users(self, faculty_user, admin_user):  # Ensure users are created
        self.faculty_user = faculty_user
        self.admin_user = admin_user

    def test_complete_submission_workflow(self, browser, live_server):
        """
        Test the complete research submission workflow from faculty login to submission.

        Feature: Research Submission

        This test verifies that faculty users can:
        1. Log in to the system
        2. Navigate to the submission form
        3. Complete the multi-step submission process
        4. Upload research files
        5. Submit a research project successfully

        The test uses Page Objects to interact with the UI and verifies
        the successful submission by checking for the success message
        and correct page redirection.
        """
        # 1. Log in as faculty
        login_page = LoginPage(browser, live_server.url)
        login_page.navigate()
        # Use fixture user credentials
        login_page.login(self.faculty_user.username, "password123")

        # Verify successful login (e.g., check URL or welcome message)
        WebDriverWait(browser, 10).until(EC.url_changes(login_page.url))
        assert "/submit/" in browser.current_url  # Assuming redirect to submit

        # 2. Navigate to the submission form (already there due to redirect)
        submission_page = SubmissionPage(browser, live_server.url)
        # No need to navigate if already redirected
        # submission_page.navigate()

        # 3. Step 1: Fill out basic information
        submission_page.fill_basic_info(
            title="Acceptance Test Research Project 12345",  # Ensure min length
            student_author="Test Accept Student",
            abstract="This is a comprehensive test abstract for the research project submission workflow. "
            "It needs to be at least 100 characters long to satisfy the validation "
            "requirements of the form. This text should be more than sufficient for that purpose.",
        )
        submission_page.go_to_next_step(SubmissionPage.NEXT_BUTTON_STEP1)

        # 4. Step 2: Fill out project details
        submission_page.fill_project_details(
            collaborators="Test Collaborator",
            date_presented="2025-03-15",
            github_link="https://github.com/testuser/test-repo",
            video_link="https://youtube.com/testvideo",
        )
        submission_page.go_to_next_step(SubmissionPage.NEXT_BUTTON_STEP2)

        # 5. Step 3: Upload research materials
        # Construct the path to the test PDF file relative to this test file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(
            os.path.join(current_dir, "..")
        )  # Up one level to research_showcase
        test_file_path = os.path.join(
            project_root, "research", "tests", "test_files", "sample.pdf"
        )

        # Check if file exists before attempting upload
        if not os.path.exists(test_file_path):
            pytest.fail(f"Test file not found at: {test_file_path}")

        # Create dummy presentation/poster files if needed, or use existing ones
        # For now, we only test PDF upload as required by the guide
        submission_page.upload_files(pdf_path=test_file_path)
        submission_page.go_to_next_step(SubmissionPage.NEXT_BUTTON_STEP3)

        # 6. Step 4: Review and submit
        submission_page.submit_project()

        # 7. Verify successful submission

        # Verify redirect to success page (already handled in submit_project wait)
        assert "/submit/success/" in browser.current_url

        # Verify success message is displayed
        success_message_locator = (By.CSS_SELECTOR, ".card-body")
        success_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located(success_message_locator)
        )
        success_text = success_element.text
        assert "successfully submitted" in success_text
        assert "pending approval" in success_text
        assert "Acceptance Test Research Project 12345" in success_text  # Verify title
