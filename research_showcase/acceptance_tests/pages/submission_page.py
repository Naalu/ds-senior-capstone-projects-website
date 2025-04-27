import os  # Import os for path operations
import time  # ADDED

from selenium.common.exceptions import (  # Import TimeoutException and NoSuchElementException
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SubmissionPage:
    """Page object for the research submission page."""

    # URL and element locators
    URL_PATH = "/submit/"  # Corresponds to name='submit_research'
    SUCCESS_URL_PATH = "/submit/success/"  # Corresponds to name='submission_success'

    # Step 1: Basic Info
    TITLE_INPUT = (By.ID, "id_title")
    STUDENT_AUTHOR_INPUT = (By.ID, "id_student_author_name")
    ABSTRACT_INPUT = (By.ID, "id_abstract")
    NEXT_BTN_STEP_1 = (
        By.XPATH,
        "//button[@onclick=\"nextStep('project-details-tab')\"]",
    )

    # Step 2: Project Details
    COLLABORATORS_INPUT = (By.ID, "id_collaborator_names")
    DATE_PRESENTED_INPUT = (By.ID, "id_date_presented")
    GITHUB_LINK_INPUT = (By.ID, "id_github_link")
    PROJECT_SPONSOR_INPUT = (By.ID, "id_project_sponsor")
    VIDEO_LINK_INPUT_STEP2 = (By.ID, "id_video_link")
    NEXT_BTN_STEP_2 = (By.XPATH, "//button[@onclick=\"nextStep('uploads-tab')\"]")
    PREV_BTN_STEP_2 = (By.XPATH, "//button[@onclick=\"nextStep('basic-info-tab')\"]")

    # Step 3: File Upload
    PDF_FILE_INPUT = (By.ID, "id_pdf_file")
    POSTER_FILE_INPUT = (By.ID, "id_poster_image")
    PRESENTATION_FILE_INPUT = (By.ID, "id_presentation_file")
    PROJECT_IMAGES_INPUT = (By.ID, "id_project_images")
    NEXT_BTN_STEP_3 = (By.XPATH, "//button[@onclick=\"nextStep('review-tab')\"]")
    PREV_BTN_STEP_3 = (
        By.XPATH,
        "//button[@onclick=\"nextStep('project-details-tab')\"]",
    )

    # Step 4: Review & Submit
    REVIEW_TITLE = (By.ID, "review-title")
    REVIEW_ABSTRACT = (By.ID, "review-abstract")
    REVIEW_STUDENT_AUTHOR = (By.ID, "review-student-author")
    SUBMIT_BUTTON = (By.XPATH, "//form[@id='researchForm']//button[@type='submit']")
    PREV_BTN_STEP_4 = (By.XPATH, "//button[@onclick=\"nextStep('uploads-tab')\"]")

    # Success indicator (on the success page)
    SUCCESS_MESSAGE_CONTAINER = (By.CSS_SELECTOR, ".card-body")

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url.rstrip("/")
        self.url = f"{self.base_url}{self.URL_PATH}"
        self.success_url = f"{self.base_url}{self.SUCCESS_URL_PATH}"

    def navigate(self):
        """Navigate directly to the submission page."""
        print(f"Navigating to submission page: {self.url}")
        self.browser.get(self.url)
        # Wait for the first step's elements to be present
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(self.TITLE_INPUT)
        )
        print("Submission page loaded (Step 1 visible).")
        return self

    def fill_basic_info(self, title, student_author, abstract):
        """Fill out the basic information step (Step 1)."""
        print("Filling basic info (Step 1)...")
        try:
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(self.TITLE_INPUT)
            ).send_keys(title)
            self.browser.find_element(*self.STUDENT_AUTHOR_INPUT).send_keys(
                student_author
            )
            self.browser.find_element(*self.ABSTRACT_INPUT).send_keys(abstract)
            print("Basic info filled.")
        except Exception as e:
            print(f"Error filling basic info: {e}")
            # self.save_debug_info("fill_basic_info_error")
            raise
        return self

    def go_to_step_2(self):
        """Click the next button to advance to Step 2 using JS click."""
        print("Clicking Next to go to Step 2...")
        try:
            next_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.NEXT_BTN_STEP_1)
            )
            self.browser.execute_script("arguments[0].click();", next_button)
            print("Clicked Step 1 Next button via JavaScript.")

            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(self.COLLABORATORS_INPUT)
            )
            print("Advanced to Step 2.")
        except Exception as e:
            print(f"Error advancing to Step 2: {e}")
            raise
        return self

    def fill_project_details(
        self,
        collaborators="",
        date_presented="",
        github_link="",
        project_sponsor="",
        video_link="",
    ):
        """Fill out the project details step (Step 2)."""
        print("Filling project details (Step 2)...")
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(self.COLLABORATORS_INPUT)
            ).send_keys(collaborators)

            if date_presented:
                date_field = self.browser.find_element(*self.DATE_PRESENTED_INPUT)
                self.browser.execute_script(
                    f"arguments[0].value = '{date_presented}';", date_field
                )
                time.sleep(0.5)

            if github_link:
                self.browser.find_element(*self.GITHUB_LINK_INPUT).send_keys(
                    github_link
                )

            if project_sponsor:
                self.browser.find_element(*self.PROJECT_SPONSOR_INPUT).send_keys(
                    project_sponsor
                )

            if video_link:
                self.browser.find_element(*self.VIDEO_LINK_INPUT_STEP2).send_keys(
                    video_link
                )

            print("Project details filled.")
        except Exception as e:
            print(f"Error filling project details: {e}")
            # self.save_debug_info("fill_project_details_error")
            raise
        return self

    def go_to_step_3(self):
        """Click the next button to advance to Step 3 using JS click."""
        print("Clicking Next to go to Step 3...")
        try:
            # Find the button first
            next_button = WebDriverWait(self.browser, 10).until(
                # Wait for presence, not clickability, as JS will handle it
                EC.presence_of_element_located(self.NEXT_BTN_STEP_2)
            )
            # Use JavaScript to click the button
            self.browser.execute_script("arguments[0].click();", next_button)
            print("Clicked Step 2 Next button via JavaScript.")

            # Wait for Step 3 specific element
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(self.PDF_FILE_INPUT)
            )
            print("Advanced to Step 3.")
        except Exception as e:
            print(f"Error advancing to Step 3: {e}")
            raise
        return self

    def upload_files(
        self,
        pdf_path=None,
        poster_path=None,
        presentation_path=None,
        project_images_paths=None,
    ):
        """Upload files in the research materials step (Step 3)."""
        print("Uploading files (Step 3)...")
        if project_images_paths is None:
            project_images_paths = []
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.PDF_FILE_INPUT)
            )

            if pdf_path:
                abs_pdf_path = os.path.abspath(pdf_path)
                print(f"Uploading PDF: {abs_pdf_path}")
                self.browser.find_element(*self.PDF_FILE_INPUT).send_keys(abs_pdf_path)

            if poster_path:
                abs_poster_path = os.path.abspath(poster_path)
                print(f"Uploading Poster: {abs_poster_path}")
                self.browser.find_element(*self.POSTER_FILE_INPUT).send_keys(
                    abs_poster_path
                )

            if presentation_path:
                abs_pres_path = os.path.abspath(presentation_path)
                print(f"Uploading Presentation: {abs_pres_path}")
                self.browser.find_element(*self.PRESENTATION_FILE_INPUT).send_keys(
                    abs_pres_path
                )

            # Handle multiple project images - gracefully skip if input not found
            if project_images_paths:
                try:
                    img_input = self.browser.find_element(*self.PROJECT_IMAGES_INPUT)
                    abs_image_paths = [os.path.abspath(p) for p in project_images_paths]
                    paths_string = "\n".join(abs_image_paths)
                    printable_paths = paths_string.replace("\n", ", ")
                    print(f"Attempting to upload Project Images: {printable_paths}")
                    img_input.send_keys(paths_string)
                    print("Project Images sent to input.")
                except NoSuchElementException:  # Import this exception
                    print(
                        "Project Images input (id_project_images) not found, skipping upload."
                    )
                except Exception as img_e:
                    print(
                        f"An unexpected error occurred during project image upload: {img_e}"
                    )
                    # Decide whether to raise or just continue

            print("Files info filled/attempted.")
        except Exception as e:
            print(f"Error uploading files: {e}")
            raise
        return self

    def go_to_step_4(self):
        """Click the next button to advance to Step 4 using JS click."""
        print("Clicking Next to go to Step 4 (Review)...")
        try:
            # Find the button first
            next_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.NEXT_BTN_STEP_3)
            )
            # Use JavaScript to click the button
            self.browser.execute_script("arguments[0].click();", next_button)
            print("Clicked Step 3 Next button via JavaScript.")

            # Wait for Step 4 specific element
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(self.REVIEW_TITLE)
            )
            print("Advanced to Step 4 (Review).")
        except Exception as e:
            print(f"Error advancing to Step 4: {e}")
            raise
        return self

    # Add methods for previous steps if needed
    def go_to_prev_step(self, target_step_element_locator):
        """Clicks the previous button and waits for the target step element."""
        print("Clicking Previous button...")
        # Determine which previous button to click based on current visibility?
        # This needs refinement based on which step we are on.
        # For now, assume we know which prev button to click
        # prev_button = self.browser.find_element(...)
        # prev_button.click()
        # WebDriverWait(self.browser, 10).until(
        #     EC.visibility_of_element_located(target_step_element_locator)
        # )
        pass  # Implement if needed

    def submit_project(self):
        """Submit the project from the review step (Step 4) using JS click."""
        print("Submitting project from Step 4...")
        try:
            # Find the submit button
            submit_button = WebDriverWait(self.browser, 10).until(
                # Wait for presence, not clickability
                EC.presence_of_element_located(self.SUBMIT_BUTTON)
            )
            # Use JavaScript to click the button
            self.browser.execute_script("arguments[0].click();", submit_button)
            print("Clicked Submit button via JavaScript.")

            # Wait for redirection to success page URL
            WebDriverWait(self.browser, 15).until(
                EC.url_contains(self.SUCCESS_URL_PATH)
            )
            print("Project submitted successfully, redirected to success page.")
        except Exception as e:
            print(f"Error submitting project: {e}")
            raise
        return self

    def get_success_message(self):
        """Get the success message text from the success page."""
        print("Getting success message...")
        try:
            # Ensure we are on the success page first
            if self.SUCCESS_URL_PATH not in self.browser.current_url:
                print("Warning: Not on the expected success page URL.")
                # return None or raise error?

            success_elem = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE_CONTAINER)
            )
            message = success_elem.text
            print(
                f"Found success message container text: '{message[:100]}...'"
            )  # Log snippet
            return message
        except TimeoutException:
            print("Error: Success message container not found on page.")
            # self.save_debug_info("get_success_message_error")
            return None
        except Exception as e:
            print(f"Error getting success message: {e}")
            return None

    # Add the debug helper from LoginPage if needed
    # def save_debug_info(self, prefix="debug"):
    #    ...

    def verify_review_data(self, expected_title, expected_author, expected_abstract):
        print("Verifying review data...")
        try:
            title_element = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located(self.REVIEW_TITLE)
            )
            assert expected_title == title_element.text

            author_element = self.browser.find_element(*self.REVIEW_STUDENT_AUTHOR)
            assert expected_author == author_element.text

            abstract_element = self.browser.find_element(*self.REVIEW_ABSTRACT)
            # Abstract might be truncated or need cleaning
            assert expected_abstract in abstract_element.text
            print("Review data verified.")
        except Exception as e:
            print(f"Error verifying review data: {e}")
            # Add screenshot/source saving here if desired
            raise
