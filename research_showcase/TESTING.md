# NAU Research Showcase Testing Guide

This document outlines the testing approach and guidelines for the NAU Mathematics & Statistics Research Showcase project.

## Verification Testing

The project uses Django's built-in testing framework with additional tools for coverage analysis.

### Running Verification Tests

To run verification tests with coverage analysis:

```bash
# Ensure you are in the research_showcase directory
cd research_showcase 
./run_tests.sh
```

This will run all tests within the `research` and `users` apps (as specified in `.coveragerc`) and generate a coverage report in the terminal and an HTML report in the `htmlcov` directory.

### Test Organization

Verification tests are organized within the `tests` package inside each app (`research`, `users`):

- `tests/test_models.py` - Tests for Django models
- `tests/test_forms.py` - Tests for form validation and logic
- `tests/test_views.py` - Tests for view functionality, permissions, and workflows
- `tests/test_utils.py` - Tests for utility functions or custom template tags (if any)

### Writing New Verification Tests

When adding new features, ensure you add appropriate tests that:

1. Follow the established structure (models, forms, views, etc.).
2. Test both success (happy path) and failure/edge cases.
3. Use mock objects (`unittest.mock`) where appropriate to isolate the component being tested from external dependencies (e.g., email sending, external APIs).
4. Verify expected outcomes, database state changes, redirects, and context data.
5. Aim to maintain or increase the overall test coverage.

## Acceptance Testing

Acceptance tests use Selenium WebDriver (via pytest-selenium) to simulate real user interactions with the application through a web browser.

### Running Acceptance Tests

To run acceptance tests from the `research_showcase` directory:

```bash
# Run ALL acceptance tests headlessly (no visible browser)
./run_acceptance_tests.sh

# Run ALL acceptance tests with a VISIBLE browser (for debugging)
./run_acceptance_tests.sh --visible

# Run a SPECIFIC test file (e.g., test_search.py) headlessly
./run_acceptance_tests.sh test_search.py

# Run a SPECIFIC test file with a VISIBLE browser
./run_acceptance_tests.sh --visible test_search.py

# Run ALL tests and generate an HTML report (acceptance_report.html)
./run_acceptance_tests.sh --html

# Combine options (e.g., specific test, visible, with report)
./run_acceptance_tests.sh --visible test_authentication.py --html
```

### Test Organization

Acceptance tests reside in the `acceptance_tests/` directory and are organized by feature:

- `acceptance_tests/test_authentication.py` - Tests for login/logout functionality
- `acceptance_tests/test_submission.py` - Tests for the research submission workflow
- `acceptance_tests/test_search.py` - Tests for search and filtering functionality

### Page Object Model

The acceptance tests use the Page Object Model (POM) pattern to separate UI interaction logic from test case logic. Page objects are located in `acceptance_tests/pages/`:

- `pages/login_page.py` - Interactions with the login page
- `pages/submission_page.py` - Interactions with the multi-step submission form
- `pages/search_page.py` - Interactions with the search interface

This pattern makes tests more readable and maintainable by encapsulating page element locators and interaction methods within dedicated classes.

### Writing New Acceptance Tests

When adding new UI features or workflows, create appropriate acceptance tests that:

1. Follow the Page Object Model pattern. Create or update page objects as needed.
2. Include clear scenario descriptions in test method docstrings.
3. Test both "happy paths" (successful interactions) and common error conditions.
4. Use explicit waits (`WebDriverWait`) instead of fixed sleeps where possible to ensure stability.
5. Verify user-visible outcomes (e.g., page content changes, success messages, redirects).
6. Add appropriate markers (`@pytest.mark.acceptance`, `@pytest.mark.feature_name`) for organization.

### Troubleshooting Acceptance Tests

If acceptance tests fail:

1. **Run with `--visible` flag:** Observe the browser interaction directly (`./run_acceptance_tests.sh --visible test_failing.py`).
2. **Check Screenshots:** Failed tests automatically save screenshots to the `screenshots/` directory. Examine the screenshot taken at the point of failure.
3. **Review Logs:** Look at the detailed console output (including `print` statements added for debugging) from the test run.
4. **Verify Locators:** Ensure element locators (IDs, CSS selectors, XPath) in the page objects still match the actual HTML structure.
5. **Check Waits:** Ensure appropriate `WebDriverWait` conditions are used before interacting with elements, especially after actions that trigger page changes or AJAX requests.
6. **Isolate the Failure:** Try running only the failing test file or class.

## Continuous Integration

The project uses GitHub Actions for continuous integration testing. The workflow defined in `.github/workflows/django.yml` automatically runs all verification and acceptance tests (headlessly) on every push and pull request to the main branches.
