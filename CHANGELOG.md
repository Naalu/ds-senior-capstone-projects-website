# Changelog

All notable changes to the NAU Mathematics & Statistics Research Showcase project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Enhanced search functionality with advanced filtering options
- Email notifications system for status changes
- Featured research section on the homepage
- Improved file preview capabilities

## [0.1.0] - Current Version

### Added

- Core Django project structure and configuration
- User authentication system with role-based access control
  - Faculty, Admin, and Visitor roles
  - Role-specific permissions and views
- Research project submission workflow
  - Form for faculty to submit student research
  - File upload capability for multiple document types
  - Research project metadata capture
- Admin approval process for submissions
  - Review interface for administrators
  - Approval/rejection functionality
  - Status tracking for submissions
- Basic templates and UI
  - Bootstrap-based responsive design with Django Template Language
  - Navigation and core page templates
  - Form styling and validation
- Models for core entities
  - User model with role definitions
  - Research project model with metadata
  - Colloquium model for presentations
- Initial documentation
  - README with setup instructions
  - Code of Conduct
  - Contributing guidelines

### Changed

- Restructured the project to follow Django best practices
- Improved navigation and user flow
- Enhanced form validation for research submissions

### Fixed

- Login and authentication redirection issues
- File upload validation and storage
- User role permission checks

## [0.0.1] - Initial Setup

### Added

- Initial project setup
- Repository creation on GitHub
- Basic requirements definition
- Project planning documents

## [0.2.0] - Upcoming Release

### Changed

- Simplified user role system to focus on Faculty and Admin roles
- Updated Faculty permissions to submit research on behalf of students
- Enhanced Admin capabilities to include all Faculty features
- Improved navigation and role-based access controls

### Removed

- Removed Student role as Faculty now submit research on behalf of students

### Added

- Basic search functionality for research projects
  - Search by title, abstract, and project sponsor
  - Results filtered to approved projects only
- Automated tests for models and views
  - Test coverage for user permissions
  - Test coverage for search functionality

