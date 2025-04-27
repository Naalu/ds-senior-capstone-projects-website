import os

import pytest
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

User = get_user_model()


@pytest.fixture(scope="session")
def browser(request):  # Added request fixture
    """Setup browser for Selenium tests."""
    chrome_options = Options()
    if request.config.getoption("--headless"):  # Check command-line option
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Often needed in CI

    # Setup ChromeDriver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        pytest.fail(f"Failed to initialize ChromeDriver: {e}")

    driver.implicitly_wait(10)

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    return User.objects.create_user(
        username="testadmin_accept",  # Use unique username
        email="admin_accept@example.com",
        password="password123",
        role="admin",
        is_staff=True,  # Ensure staff status for admin interface access
        is_superuser=True,
    )


@pytest.fixture
def faculty_user(db):
    """Create a faculty user for testing."""
    return User.objects.create_user(
        username="testfaculty_accept",  # Use unique username
        email="faculty_accept@example.com",
        password="password123",
        role="faculty",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure."""
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Only take screenshots for failed tests in the 'call' phase
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = os.path.join(
                os.path.dirname(__file__), "screenshots"
            )  # Relative path
            os.makedirs(screenshots_dir, exist_ok=True)

            # Take screenshot
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            try:
                browser.save_screenshot(screenshot_path)
                print(
                    f"\nScreenshot saved to {screenshot_path}"
                )  # Added newline for clarity
            except Exception as e:
                print(f"\nFailed to save screenshot: {e}")


# Add command line option for headless mode
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )
