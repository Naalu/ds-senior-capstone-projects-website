import os  # Add this import
import time  # Add this import for time.sleep

from selenium.common.exceptions import TimeoutException  # Import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Page object for the login page."""

    # URL and element locators
    URL_PATH = "/accounts/login/"  # Changed from /users/login based on users/urls.py
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        ".alert.alert-danger",
    )  # Updated selector based on template
    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        ".alert.alert-success",
    )  # For potential success messages

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.url = f"{base_url.rstrip('/')}{self.URL_PATH}"  # Ensure no double slash

    def navigate(self):
        """Navigate to the login page."""
        print(f"Navigating to: {self.url}")
        self.browser.get(self.url)
        # Add a wait for a known element to ensure page is loaded
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.USERNAME_INPUT)
            )
            print("Login page loaded.")
        except TimeoutException:
            print(f"Error: Login page did not load correctly at {self.url}")
            # Optionally raise an error or handle it
            raise TimeoutException(
                f"Login page failed to load element {self.USERNAME_INPUT}"
            )
        return self

    def login(self, username, password):
        """Perform login with the provided credentials."""
        print(f"Attempting login with username: {username}")

        try:
            # Wait for elements to be present and interactable
            username_field = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(self.USERNAME_INPUT)
            )
            password_field = self.browser.find_element(*self.PASSWORD_INPUT)
            submit_button = self.browser.find_element(*self.SUBMIT_BUTTON)

            # Clear and enter username
            username_field.clear()
            username_field.send_keys(username)

            # Clear and enter password
            password_field.clear()
            password_field.send_keys(password)

            # Click login button
            print("Clicking login button...")
            submit_button.click()

            # Add a small explicit delay after click before checking state
            time.sleep(0.5)  # Wait half a second

            # Wait for URL change OR error message to appear
            print("Waiting for URL change or error message...")
            WebDriverWait(self.browser, 10).until(
                EC.any_of(
                    EC.url_changes(self.url),
                    EC.presence_of_element_located(self.ERROR_MESSAGE),
                )
            )

            print(f"Login attempt completed. Current URL: {self.browser.current_url}")

        except TimeoutException:
            print(
                "Timeout occurred during login process. Page might not have transitioned or error not shown."
            )
            # You might want to raise an error here or return a failure status
            raise
        except Exception as e:
            print(f"An unexpected error occurred during login: {e}")
            # Consider saving page source for debugging
            # self.save_debug_info("login_error")
            raise

        return self  # Return self for chaining

    def get_error_message(self):
        """Get the error message if login failed."""
        try:
            # Wait briefly for the error message element to be present
            error_element = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            message = error_element.text
            print(f"Found error message: '{message}'")
            return message
        except TimeoutException:
            print("No error message found on the page.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting error message: {e}")
            return None

    def get_success_message(self):
        """Get the success message if one appears (e.g., after logout)."""
        try:
            # Wait briefly for the success message element to be present
            success_element = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            message = success_element.text
            print(f"Found success message: '{message}'")
            return message
        except TimeoutException:
            print("No success message found on the page.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting success message: {e}")
            return None

    def is_login_page(self):
        """Check if currently on the login page by URL."""
        on_page = self.URL_PATH in self.browser.current_url
        print(f"Checking if on login page ({self.URL_PATH}): {on_page}")
        return on_page

    def wait_for_page_load(self, expected_element_locator=None, timeout=10):
        """Wait for a specific element to be present after navigation or action."""
        if not expected_element_locator:
            # Default wait for body tag if no specific element is given
            expected_element_locator = (By.TAG_NAME, "body")
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(expected_element_locator)
            )
            print(
                f"Page loaded successfully (found element {expected_element_locator})."
            )
        except TimeoutException:
            print(
                f"Timeout waiting for page load (element {expected_element_locator} not found). Current URL: {self.browser.current_url}"
            )
            raise

    def save_debug_info(self, prefix="debug"):
        """Save page source and screenshot for debugging."""
        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        debug_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "debug_output"
        )
        os.makedirs(debug_dir, exist_ok=True)

        # Save page source
        source_path = os.path.join(debug_dir, f"{prefix}_{timestamp}.html")
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(self.browser.page_source)
        print(f"Saved page source to {source_path}")

        # Save screenshot
        screenshot_path = os.path.join(debug_dir, f"{prefix}_{timestamp}.png")
        try:
            self.browser.save_screenshot(screenshot_path)
            print(f"Saved screenshot to {screenshot_path}")
        except Exception as e:
            print(f"Failed to save screenshot: {e}")

    def get_current_page_source(self):
        """Get the current page source (for debugging)."""
        return self.browser.page_source
