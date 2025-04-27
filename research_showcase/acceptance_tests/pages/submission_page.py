import os  # Needed for file uploads

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SubmissionPage:
    """Page object for the research submission page (multi-step)."""

    # Step 1: Basic Information Locators
    TITLE_INPUT = (By.ID, "id_step1-title")  # IDs adjusted for form wizard
    STUDENT_AUTHOR_INPUT = (By.ID, "id_step1-student_author_name")
    ABSTRACT_TEXTAREA = (By.ID, "id_step1-abstract")
    NEXT_BUTTON_STEP1 = (By.XPATH, "//button[contains(text(), 'Next')]")

    # Step 2: Project Details Locators
    COLLABORATORS_INPUT = (By.ID, "id_step2-collaborator_names")
    DATE_PRESENTED_INPUT = (By.ID, "id_step2-date_presented")
    GITHUB_LINK_INPUT = (By.ID, "id_step2-github_link")
    VIDEO_LINK_INPUT = (By.ID, "id_step2-video_link")  # Added based on form
    NEXT_BUTTON_STEP2 = (By.XPATH, "//button[contains(text(), 'Next')]")

    # Step 3: Research Materials Locators
    PDF_FILE_INPUT = (By.ID, "id_step3-pdf_file")
    PRESENTATION_FILE_INPUT = (By.ID, "id_step3-presentation_file")  # Added
    POSTER_IMAGE_INPUT = (By.ID, "id_step3-poster_image")  # Added
    NEXT_BUTTON_STEP3 = (By.XPATH, "//button[contains(text(), 'Next')]")

    # Step 4: Review & Submit Locators
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Submit Research')]")

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.url = f"{base_url}/submit/"  # Use base_url

    def navigate(self):
        """Navigate to the submission page."""
        self.browser.get(self.url)
        # Wait for title input to be present
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(self.TITLE_INPUT)
        )
        return self

    def fill_basic_info(self, title, student_author, abstract):
        """Fill out the basic information step."""
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.TITLE_INPUT)
        )
        self.browser.find_element(*self.TITLE_INPUT).send_keys(title)
        self.browser.find_element(*self.STUDENT_AUTHOR_INPUT).send_keys(student_author)
        self.browser.find_element(*self.ABSTRACT_TEXTAREA).send_keys(abstract)
        return self

    def go_to_next_step(self, current_step_button_locator):
        """Click the 'Next' button for the current step."""
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(current_step_button_locator)
        ).click()
        return self

    def fill_project_details(
        self, collaborators="", date_presented="", github_link="", video_link=""
    ):
        """Fill out the project details step."""
        # Wait for the project details form to be visible
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.COLLABORATORS_INPUT)
        )
        self.browser.find_element(*self.COLLABORATORS_INPUT).send_keys(collaborators)
        if date_presented:
            # Handle date input - might need specific format or picker interaction
            date_input = self.browser.find_element(*self.DATE_PRESENTED_INPUT)
            date_input.clear()
            date_input.send_keys(date_presented)  # Assumes YYYY-MM-DD
        if github_link:
            self.browser.find_element(*self.GITHUB_LINK_INPUT).send_keys(github_link)
        if video_link:
            self.browser.find_element(*self.VIDEO_LINK_INPUT).send_keys(video_link)
        return self

    def upload_files(self, pdf_path=None, presentation_path=None, poster_path=None):
        """Upload files in the research materials step."""
        # Wait for the file upload form to be visible
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.PDF_FILE_INPUT)
        )

        # Use absolute paths for send_keys with file inputs
        if pdf_path:
            abs_pdf_path = os.path.abspath(pdf_path)
            self.browser.find_element(*self.PDF_FILE_INPUT).send_keys(abs_pdf_path)
        if presentation_path:
            abs_pres_path = os.path.abspath(presentation_path)
            self.browser.find_element(*self.PRESENTATION_FILE_INPUT).send_keys(
                abs_pres_path
            )
        if poster_path:
            abs_poster_path = os.path.abspath(poster_path)
            self.browser.find_element(*self.POSTER_IMAGE_INPUT).send_keys(
                abs_poster_path
            )
        return self

    def submit_project(self):
        """Submit the project from the review step."""
        # Wait for the submit button to be clickable
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON)
        ).click()
        # Wait for redirection to success page or confirmation message
        WebDriverWait(self.browser, 15).until(EC.url_contains("/submit/success/"))
        return self
