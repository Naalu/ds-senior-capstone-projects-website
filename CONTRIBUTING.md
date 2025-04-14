# Contributing to NAU Research Showcase

Thank you for considering contributing to the NAU Mathematics & Statistics Research Showcase! This document outlines the process for contributing to the project and guidelines for development.

## Table of Contents

- [Contributing to NAU Research Showcase](#contributing-to-nau-research-showcase)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Pull Request Process](#pull-request-process)
  - [Code Style Guidelines](#code-style-guidelines)
  - [Testing Guidelines](#testing-guidelines)
  - [Documentation Guidelines](#documentation-guidelines)
  - [Questions?](#questions)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Set up the development environment**:
   - Follow the installation steps in the [README.md](README.md)
   - Make sure all tests pass before making changes
4. **Create a new branch** for your feature or bugfix
5. **Make your changes** and commit them
6. **Push your branch** to your fork
7. **Submit a pull request** to the main repository

## Development Workflow

1. **Check the issue tracker** for open issues or create a new one
2. **Assign yourself** to the issue you're working on
3. **Create a feature branch** from the `main` branch
4. **Implement your changes** with appropriate tests
5. **Ensure tests pass** and meet code coverage requirements
6. **Update documentation** as needed
7. **Submit a pull request** for review

## Branching Strategy

We use a simplified Git workflow:

- **`main`**: The primary branch containing the stable codebase
- **`feature/*`**: Feature branches for new features or enhancements (e.g., `feature/search-functionality`)
- **`bugfix/*`**: Branches for bug fixes (e.g., `bugfix/login-error`)
- **`docs/*`**: Branches for documentation updates (e.g., `docs/api-documentation`)

## Pull Request Process

1. **Create a pull request** from your feature branch to the `main` branch
2. **Fill out the pull request template** with details about your changes
3. **Request a review** from at least one team member
4. **Address review comments** and make necessary changes
5. **Ensure all checks pass** (tests, linting, etc.)
6. **Wait for approval** before merging

Your pull request will be reviewed by at least one team member and must receive approval before merging.

## Code Style Guidelines

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Additionally:

- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters
- Use meaningful variable and function names
- Include docstrings for all functions, classes, and modules
- Add comments for complex logic

For frontend code:

- Follow HTML5 standards
- Use Django Template Language (DTL) for template rendering
- Apply Bootstrap classes consistently for styling
- Keep CSS organized with clear naming conventions

## Testing Guidelines

This section outlines the testing strategy used for the NAU Mathematics & Statistics Research Showcase application.

### Overview

We utilize Django's built-in testing framework, which is based on Python's standard `unittest` module. Our goal is to ensure the reliability and correctness of the application through a combination of unit and integration tests.

### Test Suite Structure

Tests are organized within each Django app (`research`, `users`) in their respective `tests.py` files. Each test file contains test classes inheriting from `django.test.TestCase`, which provides useful assertions and a test client for simulating requests.

### Types of Tests

- **Unit Tests:** Focus on testing individual components in isolation, such as:
  - Model methods and properties (`research/models.py`, `users/models.py`)
  - Form validation logic (`research/forms.py`, `users/forms.py`)
  - Decorators (`users/decorators.py`)
  - Utility functions (e.g., `research/semester_utils.py`)
- **Integration Tests:** Verify the interaction between different parts of the application, primarily focusing on:
  - View logic and responses (`research/views.py`, `users/views.py`)
  - URL routing (`research/urls.py`, `users/urls.py`)
  - User workflows (e.g., login, logout, research submission, approval process, profile editing)
- **UI Tests:** *(Currently Not Implemented)* Tests that interact with the application through a web browser (e.g., using Selenium or Playwright) are not yet part of the suite but could be added in the future to test user journeys directly in the frontend.

### Running Tests

Tests can be run from the root of the `research_showcase` directory (the one containing `manage.py`) after activating the virtual environment.

1. **Run all tests:**

    ```bash
    python manage.py test
    ```

2. **Run tests for a specific app:**

    ```bash
    python manage.py test research
    # or
    python manage.py test users
    ```

### Test Coverage

We use the `coverage` package to measure test coverage.

1. **Run tests with coverage:**

    ```bash
    # Make sure you are in the research_showcase directory
    python -m coverage run manage.py test
    ```

2. **View coverage report:**

    ```bash
    coverage report
    ```

    *(Generates a summary in the terminal)*

3. **Generate HTML report (for detailed view):**

    ```bash
    coverage html
    ```

    *(Creates an `htmlcov/` directory; open `htmlcov/index.html` in a browser)*

**Target Coverage:** The project aims for a minimum of 70% test coverage, with a goal of exceeding 95% where practical. As of [Date - You can fill this in], the overall coverage is **95%**.

### Continuous Integration (CI)

A GitHub Actions workflow is configured in `.github/workflows/django.yml`. This workflow automatically runs the full test suite (`python manage.py test`) on every push and pull request to the `main` branch, ensuring that code changes do not introduce regressions.

### Maintainability

Tests are written to be clear, understandable, and maintainable. Test methods focus on verifying specific functionalities or behaviors. Test setup uses the `setUp` method within test classes where appropriate to avoid code duplication.

## Documentation Guidelines

- Update documentation for any changed functionality
- Document all models, views, forms, and URLs
- Write clear docstrings following the Google Python Style Guide
- Maintain consistency between code comments and external documentation
- Update the README and other documentation files when necessary

## Questions?

If you have any questions or need help with the contribution process, please reach out to the project maintainers through the GitHub issue tracker.

Thank you for contributing to the NAU Mathematics & Statistics Research Showcase!
