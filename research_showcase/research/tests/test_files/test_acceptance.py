from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
import time

class BasicAcceptanceTest(StaticLiveServerTestCase):
    def setUp(self):
        service = Service(executable_path=r"C:\Users\ewf08\Downloads\chromedriver-win32.zip\chromedriver-win32")  # 👈 this is the path to driver in your device
        self.browser = webdriver.Chrome(service=service)

    def tearDown(self):
        self.browser.quit()

    def test_homepage_loads(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Welcome', body.text)
