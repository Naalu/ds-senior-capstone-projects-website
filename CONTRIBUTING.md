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

- Write tests for all new features and bug fixes
- Aim for at least 70% code coverage
- Use Django's built-in testing framework
- Organize tests to mirror the structure of the application
- Test models, views, forms, and URLs separately

To run tests:

```bash
python manage.py test
```

To run tests with coverage report:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Documentation Guidelines

- Update documentation for any changed functionality
- Document all models, views, forms, and URLs
- Write clear docstrings following the Google Python Style Guide
- Maintain consistency between code comments and external documentation
- Update the README and other documentation files when necessary

## Questions?

If you have any questions or need help with the contribution process, please reach out to the project maintainers through the GitHub issue tracker.

Thank you for contributing to the NAU Mathematics & Statistics Research Showcase!
