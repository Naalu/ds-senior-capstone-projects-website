from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SuperUserLoginSeleniumTest(StaticLiveServerTestCase):

    def setUp(self):
        # Use the existing superuser's credentials
        self.username = 'ewf25'  # Replace with your actual superuser username
        self.password = 'Riven001'  # Replace with your actual superuser password

        # Set up the Selenium WebDriver
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_superuser_login(self):
        # Go to the admin login page
        self.browser.get(self.live_server_url + '/admin/login/')  # Change the URL if necessary

        # Find the username and password fields
        username_field = self.browser.find_element(By.NAME, 'username')
        password_field = self.browser.find_element(By.NAME, 'password')

        # Enter the superuser credentials
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        # Submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(2)  # Adjust wait time or use WebDriverWait for a more reliable solution

        # Check if the admin page is loaded (check for something only visible to logged-in users)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Site administration', body.text)  # Check for admin-specific content