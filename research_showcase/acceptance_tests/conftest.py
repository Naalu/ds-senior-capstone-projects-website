import datetime  # Import datetime
import os

import pytest
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

User = get_user_model()


@pytest.fixture(scope="session")
def browser(request):
    """Setup browser for Selenium tests using local ChromeDriver."""
    print("Setting up Chrome WebDriver using local driver...")
    chrome_options = Options()

    # Add --headless argument only if the flag is explicitly true
    if request.config.getoption("--headless"):
        print("Configuring for headless mode.")
        chrome_options.add_argument("--headless")
    else:
        print("Configuring for visible mode.")

    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Dynamically find ChromeDriver in the drivers directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    drivers_dir = os.path.join(base_dir, "drivers")
    driver_filename = None
    try:
        # Find the first non-hidden file in the drivers directory
        for f in os.listdir(drivers_dir):
            if not f.startswith("."):  # Basic check to ignore hidden files
                driver_filename = f
                break  # Use the first one found
        if driver_filename is None:
            pytest.fail(f"No ChromeDriver executable found in directory: {drivers_dir}")

        driver_path = os.path.join(drivers_dir, driver_filename)
        print(f"Using local ChromeDriver found at: {driver_path}")

    except FileNotFoundError:
        pytest.fail(f"Drivers directory not found at: {drivers_dir}")
    except Exception as e:
        pytest.fail(f"Error finding ChromeDriver in {drivers_dir}: {e}")

    # Check existence and permissions
    if not os.path.exists(driver_path):
        pytest.fail(
            f"ChromeDriver path determined ({driver_path}), but file does not exist."
        )  # Should not happen if found by listdir
    if not os.access(driver_path, os.X_OK):
        pytest.fail(
            f"ChromeDriver at {driver_path} is not executable. Run 'chmod +x <path_to_driver>'."
        )

    # Setup ChromeDriver service
    service = Service(executable_path=driver_path)

    driver = None  # Initialize driver to None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)  # Set implicit wait after successful initialization

        # Add helpful debug information
        print(
            f"Browser session started - {'headless' if request.config.getoption('--headless') else 'visible'} mode"
        )

        yield driver

    finally:
        # Cleanup
        if driver:
            print("Closing browser session...")
            driver.quit()
        else:
            print("Browser session failed to start.")


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    return User.objects.create_user(
        username="testadmin",
        email="admin@example.com",
        password="password123",
        role="admin",
    )


@pytest.fixture
def faculty_user(db):
    """Create a faculty user for testing."""
    return User.objects.create_user(
        username="testfaculty",
        email="faculty@example.com",
        password="password123",
        role="faculty",
    )


# Add command line option to run tests in headless mode or not
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,  # Default to visible mode
        help="Run browser in headless mode (visible is default)",
    )


# Screenshot capture on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Check if 'browser' fixture is used in the test
        browser_fixture = item.funcargs.get("browser")
        if browser_fixture is not None:
            # Create screenshots directory if it doesn't exist (relative to project root)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            screenshots_dir = os.path.join(base_dir, "screenshots")  # Use base_dir
            os.makedirs(screenshots_dir, exist_ok=True)

            # Take screenshot with timestamp and test name
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            # Sanitize item.name for filename
            sanitized_test_name = "".join(c if c.isalnum() else "_" for c in item.name)
            screenshot_path = os.path.join(
                screenshots_dir, f"{sanitized_test_name}-{timestamp}.png"
            )
            try:
                browser_fixture.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
            except Exception as e:
                print(f"Failed to save screenshot: {e}")
        else:
            print("'browser' fixture not found, cannot take screenshot.")


# Create test database with necessary content
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up test database with necessary content."""
    with django_db_blocker.unblock():
        # Setup could include creating categories, projects, etc.
        print("Setting up test database...")  # Add print statement
        # Example: Create a default category if needed for tests
        # from research.models import Category
        # Category.objects.get_or_create(name="General")
        pass
    print("Test database setup complete.")  # Add print statement


# Make the live_server fixture available
