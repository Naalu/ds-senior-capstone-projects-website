from datetime import date, timedelta
from urllib.parse import urlencode

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from research.models import ResearchProject
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from acceptance_tests.pages.search_page import SearchPage

User = get_user_model()


@pytest.mark.acceptance
@pytest.mark.search  # Add search marker
class TestSearchFunctionality:
    """
    Acceptance tests for the search and filtering functionality.

    These tests verify that users can search for and filter research projects.
    """

    @pytest.fixture
    def create_test_projects(self, db):
        """Create test projects for search testing."""
        # Create a faculty user for the projects
        faculty = User.objects.create_user(
            username="searchfaculty",
            email="searchfaculty@example.com",
            password="password123",
            role="faculty",
        )

        # Calculate dates for different semesters
        today = date.today()
        spring_date = date(today.year, 3, 15)
        fall_date = date(today.year, 10, 15)

        # Create approved projects
        projects = [
            ResearchProject.objects.create(
                title="Machine Learning Analysis",
                abstract="A study of machine learning algorithms",
                author=faculty,
                student_author_name="ML Researcher",
                approval_status="approved",
                date_presented=spring_date,
            ),
            ResearchProject.objects.create(
                title="Statistical Methods in Biology",
                abstract="Applying statistics to biological datasets",
                author=faculty,
                student_author_name="Bio Statistician",
                approval_status="approved",
                date_presented=fall_date,
            ),
            ResearchProject.objects.create(
                title="Data Visualization Techniques",
                abstract="Modern approaches to data visualization",
                author=faculty,
                student_author_name="Viz Designer",
                approval_status="approved",
                date_presented=spring_date - timedelta(days=365),  # Previous year
            ),
        ]

        # Create a pending project that shouldn't appear in results
        ResearchProject.objects.create(
            title="Pending Project",
            abstract="This project is still pending",
            author=faculty,
            student_author_name="Pending Student",
            approval_status="pending",
            date_presented=today,
        )

        print(f"Created {len(projects)} approved test projects and 1 pending.")
        return projects

    def test_search_page_loads(self, browser, live_server):
        """Test that the search page loads correctly."""
        search_page = SearchPage(browser, live_server.url)
        search_page.navigate()

        # Verify search form is present
        assert (
            WebDriverWait(browser, 5)
            .until(EC.presence_of_element_located(search_page.SEARCH_INPUT))
            .is_displayed()
        )
        assert (
            WebDriverWait(browser, 5)
            .until(EC.presence_of_element_located(search_page.SEARCH_BUTTON))
            .is_displayed()
        )
        assert (
            WebDriverWait(browser, 5)
            .until(EC.presence_of_element_located(search_page.START_SEMESTER_SELECT))
            .is_displayed()
        )
        assert (
            WebDriverWait(browser, 5)
            .until(EC.presence_of_element_located(search_page.END_SEMESTER_SELECT))
            .is_displayed()
        )

        print("(Test) Search page loaded successfully.")

    def test_keyword_search(self, browser, live_server, create_test_projects):
        """
        Test keyword search functionality.

        This test verifies that the search function correctly filters
        research projects based on keywords in title or abstract.
        It also implicitly checks that only approved projects are shown.
        """
        search_page = SearchPage(browser, live_server.url)
        search_page.navigate()

        # Search for "machine learning"
        search_page.search_for("machine learning")

        # Verify results
        titles = search_page.get_result_titles()
        count = search_page.get_result_count()
        assert count == 1, f"Expected 1 result for 'machine learning', found {count}"
        assert "Machine Learning Analysis" in titles
        assert "Statistical Methods in Biology" not in titles
        assert "Data Visualization Techniques" not in titles
        assert "Pending Project" not in titles  # Check pending is excluded

        # Reset and search for "statistics"
        search_page.navigate()  # Go back to search page
        search_page.search_for("statistics")

        # Verify different results
        titles = search_page.get_result_titles()
        count = search_page.get_result_count()
        assert count == 1, f"Expected 1 result for 'statistics', found {count}"
        assert "Statistical Methods in Biology" in titles
        assert "Machine Learning Analysis" not in titles

        # Search for term present in multiple projects
        search_page.navigate()
        search_page.search_for("data")  # Should match biology and visualization

        titles = search_page.get_result_titles()
        count = search_page.get_result_count()
        assert count == 2, f"Expected 2 results for 'data', found {count}"
        assert "Statistical Methods in Biology" in titles
        assert "Data Visualization Techniques" in titles
        assert "Machine Learning Analysis" not in titles

        print("(Test) Keyword search is working correctly.")

    # Add test for semester filtering
    def test_semester_filter(self, browser, live_server, create_test_projects):
        """Test filtering by semester range."""
        search_page = SearchPage(browser, live_server.url)
        search_page.navigate()

        # Get current year for dynamic semester generation
        current_year = date.today().year
        spring_semester = f"Spring {current_year}"
        fall_semester = f"Fall {current_year}"
        search_url_base = f"{live_server.url}{reverse('search_research')}"

        # --- Filter for Spring semester of current year ---
        print(f"\nTesting filter: {spring_semester} to {spring_semester}")
        # Set dropdowns visually first (might not be strictly necessary anymore but good for visual debug)
        search_page.set_date_range(spring_semester, spring_semester)
        # Construct URL and navigate directly
        params = {
            "start_semester": spring_semester,
            "end_semester": spring_semester,
            "q": "",
        }
        filter_url = f"{search_url_base}?{urlencode(params)}"
        print(f"Navigating directly to: {filter_url}")
        browser.get(filter_url)
        # Wait for results container to load after navigation
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(search_page.RESULTS_CONTAINER)
        )

        titles = search_page.get_result_titles()
        count = search_page.get_result_count()
        assert count == 1, (
            f"FAIL Spring->Spring: Expected 1, Found {count}, Titles: {titles}"
        )
        assert "Machine Learning Analysis" in titles

        # --- Filter for Fall semester of current year ---
        print(f"\nTesting filter: {fall_semester} to {fall_semester}")
        search_page.set_date_range(fall_semester, fall_semester)
        params = {
            "start_semester": fall_semester,
            "end_semester": fall_semester,
            "q": "",
        }
        filter_url = f"{search_url_base}?{urlencode(params)}"
        print(f"Navigating directly to: {filter_url}")
        browser.get(filter_url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(search_page.RESULTS_CONTAINER)
        )

        titles = search_page.get_result_titles()
        count = search_page.get_result_count()
        assert count == 1, (
            f"FAIL Fall->Fall: Expected 1, Found {count}, Titles: {titles}"
        )
        assert "Statistical Methods in Biology" in titles

        # --- Filter for range including both spring and fall of current year ---
        print(f"\nTesting filter: {spring_semester} to {fall_semester}")
        search_page.set_date_range(spring_semester, fall_semester)
        params = {
            "start_semester": spring_semester,
            "end_semester": fall_semester,
            "q": "",
        }
        filter_url = f"{search_url_base}?{urlencode(params)}"
        print(f"Navigating directly to: {filter_url}")
        browser.get(filter_url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(search_page.RESULTS_CONTAINER)
        )

        titles = search_page.get_result_titles()
        count = search_page.get_result_count()
        assert count == 2, (
            f"FAIL Spring->Fall: Expected 2, Found {count}, Titles: {titles}"
        )
        assert "Machine Learning Analysis" in titles
        assert "Statistical Methods in Biology" in titles

        print("(Test) Semester filtering working correctly.")
