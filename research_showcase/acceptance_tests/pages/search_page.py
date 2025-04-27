from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,  # Added StaleElementReferenceException
    TimeoutException,  # Import TimeoutException and NoSuchElementException; ADDED
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class SearchPage:
    """Page object for the search page."""

    # URL and element locators
    URL_PATH = "/search/"
    SEARCH_INPUT = (By.NAME, "q")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    START_SEMESTER_SELECT = (By.ID, "start_semester")
    END_SEMESTER_SELECT = (By.ID, "end_semester")
    RESULTS_CONTAINER = (By.ID, "project-list-container")
    PROJECT_ITEMS = (By.CSS_SELECTOR, ".project-item")

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        self.url = f"{self.base_url}{self.URL_PATH}"

    def navigate(self):
        """Navigate to the search page."""
        print(f"Navigating to search page: {self.url}")
        self.browser.get(self.url)
        # Wait for search input to confirm page load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        print("Search page loaded successfully.")
        return self

    def search_for(self, query):
        """Perform a search with the given query."""
        print(f"Searching for: {query}")
        try:
            search_input = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(query)

            # Click search button
            search_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(self.SEARCH_BUTTON)
            )
            search_button.click()

            # Wait for results container to be present (might be empty)
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.RESULTS_CONTAINER)
            )
            print("Search submitted, results container present.")
        except Exception as e:
            print(f"Error during search_for: {e}")
            # Add debug saving if needed
            raise
        return self

    def set_date_range(self, start_semester, end_semester):
        """Set the date range filters."""
        print(f"Setting date range: {start_semester} to {end_semester}")
        try:
            if start_semester:
                start_select_elem = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable(self.START_SEMESTER_SELECT)
                )
                start_select = Select(start_select_elem)
                start_select.select_by_visible_text(start_semester)
                print(f"Selected start semester: {start_semester}")

            if end_semester:
                end_select_elem = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable(self.END_SEMESTER_SELECT)
                )
                end_select = Select(end_select_elem)
                end_select.select_by_visible_text(end_semester)
                print(f"Selected end semester: {end_semester}")
        except Exception as e:
            print(f"Error setting date range: {e}")
            raise
        return self

    def apply_filters(self):
        """Apply the current filters by clicking search button."""
        print("Applying filters (clicking search)...")
        try:
            search_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(self.SEARCH_BUTTON)
            )
            search_button.click()

            # Wait for results to refresh/potentially change
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.RESULTS_CONTAINER)
            )
            print("Filters applied, results container present.")
        except Exception as e:
            print(f"Error applying filters: {e}")
            raise
        return self

    def get_result_count(self):
        """Get the number of search results currently displayed."""
        try:
            # Wait briefly for items to appear if results just loaded
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located(self.PROJECT_ITEMS)
            )
            results = self.browser.find_elements(*self.PROJECT_ITEMS)
            count = len(results)
            print(f"Found {count} project items.")
            return count
        except TimeoutException:
            # If no items found after wait, assume 0 results
            print("No project items found.")
            return 0
        except Exception as e:
            print(f"Error getting result count: {e}")
            return 0  # Or raise? Depends on desired test behavior

    def get_result_titles(self):
        """Get the titles of all displayed search results."""
        titles = []
        print("Getting result titles...")
        try:
            # Wait for the container to be present
            results_container = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.RESULTS_CONTAINER)
            )
            # Find initial project items within the container
            initial_items = results_container.find_elements(*self.PROJECT_ITEMS)
            num_items = len(initial_items)
            print(f"Found {num_items} potential project items initially.")

            for i in range(num_items):
                try:
                    # Re-find the specific item using its index/position if possible,
                    # or re-find all items and get the i-th one.
                    # Re-finding all is safer if the DOM structure changes significantly.
                    current_items = results_container.find_elements(*self.PROJECT_ITEMS)
                    if i < len(current_items):
                        result_item = current_items[i]
                        # Now wait for and get the title from this potentially refreshed item
                        title_element = WebDriverWait(result_item, 5).until(
                            EC.visibility_of_element_located(
                                (By.CSS_SELECTOR, "h5.card-title")
                            )
                        )
                        title_text = title_element.text
                        titles.append(title_text)
                        print(f"  Item {i}: Found title '{title_text}'")
                    else:
                        print(
                            f"  Item {i}: Could not re-find item, list length changed?"
                        )
                        titles.append("ITEM NOT FOUND")

                except (
                    NoSuchElementException,
                    TimeoutException,
                    StaleElementReferenceException,
                ) as inner_e:
                    print(
                        f"  Item {i}: Could not find title or item became stale: {type(inner_e).__name__}"
                    )
                    titles.append("TITLE NOT FOUND")
            print(f"Extracted titles: {titles}")
        except TimeoutException:
            print("Project items container not found.")
        except Exception as e:
            print(f"Error getting result titles: {e}")
        return titles
