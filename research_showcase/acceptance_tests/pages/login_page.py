from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Page object for the login page."""

    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.url = f"{base_url}/accounts/login/"  # Use base_url

    def navigate(self):
        """Navigate to the login page."""
        self.browser.get(self.url)
        # Wait for username input to be present to ensure page is loaded
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        return self

    def login(self, username, password):
        """Log in with the given credentials."""
        self.browser.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.browser.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.browser.find_element(*self.SUBMIT_BUTTON).click()
        # Add a small wait for potential redirect or error message
        WebDriverWait(self.browser, 5).until(
            lambda driver: driver.current_url != self.url
            or EC.presence_of_element_located(self.ERROR_MESSAGE)(driver)
        )
        return self

    def get_error_message(self):
        """Get the error message if login failed."""
        try:
            # Wait briefly for the error message to appear
            element = WebDriverWait(self.browser, 2).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return element.text
        except:
            return None
