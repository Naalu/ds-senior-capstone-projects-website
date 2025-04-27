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

Acceptance tests use [Selenium WebDriver](https://www.selenium.dev/) and [pytest](https://docs.pytest.org/) to simulate real user interactions with the application's web interface.

### Running Acceptance Tests

To run acceptance tests and generate an HTML report:

```bash
# Ensure you are in the research_showcase directory
cd research_showcase
./run_acceptance_tests.sh
```

This will run all tests marked with `@pytest.mark.acceptance` within the `acceptance_tests` directory and generate an HTML report at `acceptance_tests/acceptance_report.html`.

To run in headless mode (without opening a visible browser window), use:

```bash
./run_acceptance_tests.sh --headless
```

### Test Organization

Acceptance tests reside in the `research_showcase/acceptance_tests` directory:

- `conftest.py` - Contains shared fixtures (like the browser setup) and hooks (like screenshot on failure).
- `pages/` - Contains Page Object Model classes representing different application pages.
- `test_*.py` - Test files containing test scenarios, organized by feature (e.g., `test_submission.py`, `test_authentication.py`).

### Page Object Model (POM)

The acceptance tests use the Page Object Model pattern. Each class in the `pages/` directory represents a specific page or significant component of the UI. These classes encapsulate the locators (e.g., CSS selectors, IDs) and methods needed to interact with that page's elements.

This pattern separates page interaction logic from test assertion logic, making tests more readable and maintainable. If the UI structure changes, updates are primarily needed within the relevant page object class, not scattered across multiple test files.

### Writing New Acceptance Tests

When adding new UI features or testing existing ones:

1. Identify the pages involved in the user workflow.
2. Create or update the corresponding Page Object classes in the `pages/` directory, adding necessary locators and interaction methods.
3. Create a new test file (e.g., `test_feature.py`) or add to an existing one.
4. Write test functions within a test class (e.g., `TestFeatureWorkflow`).
5. Use the `@pytest.mark.acceptance` marker.
6. Use the `browser` and `live_server` fixtures provided by `pytest-django` and `conftest.py`.
7. Instantiate necessary Page Objects and use their methods to drive the browser interactions.
8. Use `assert` statements to verify expected outcomes (e.g., page content, URL changes, element visibility).
9. Include clear docstrings explaining the purpose and steps of the test scenario.
