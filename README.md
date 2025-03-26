# NAU Mathematics & Statistics Research Showcase

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://semver.org)

A web-based platform designed to organize, archive, and showcase student research within Northern Arizona University's Department of Mathematics & Statistics.

## Overview

The **NAU Mathematics & Statistics Research Showcase** is a centralized platform that transforms how student research is managed and shared within the department. It provides:

- A structured repository where **faculty submit** student research
- A quality control process where **administrators approve** submissions
- A searchable archive where **visitors discover** valuable research

By making research projects easily accessible, the platform increases research visibility, enhances student portfolios, and helps faculty reference past work—creating value for students, faculty, and external audiences.

## Core Features

- **Faculty-Driven Research Submission** – Faculty submit student research with complete metadata and file attachments
- **Admin Review & Approval** – Administrators ensure quality control through a structured review process
- **Advanced Search & Filtering** – Find research by title, category, advisor, or keywords
- **Public Research Repository** – Browse approved projects in a well-organized archive
- **Secure Role-Based Access** – Different capabilities for faculty and administrators
- **Streamlined Management** – Intuitive interfaces for all user roles

## User Roles

The platform features two primary user roles:

- **Faculty** – Submit and manage research projects on behalf of students
- **Administrators** – Review, approve, and manage all research submissions

## Quick Start

### Prerequisites

- Python 3.10+
- pip package manager

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Naalu/ds-senior-capstone-projects-website.git
cd ds-senior-capstone-projects-website/research_showcase
```

2. **Create and activate a virtual environment**

**macOS/Linux**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply database migrations**

```bash
python manage.py migrate
```

5. **Create a superuser (admin account)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

7. **Access the application**

- Frontend: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Documentation

- [Usage Guide](USAGE.md) - How to use the application
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
- [Changelog](CHANGELOG.md) - Version history and changes
- [Project Design](docs/DESIGN.md) - Architecture and design decisions

## Tech Stack

- **Backend**: Django 5.1.6 (Python)
- **Database**: SQLite (development)
- **Frontend**: HTML/CSS with Bootstrap
- **Template Engine**: Django Template Language (DTL)
- **Version Control**: Git/GitHub

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Team

This project is developed by:

- Ethan Ferguson
- Jack Tomlon
- Karl Reger
- Rylan Harris-Small

Northern Arizona University, Department of Mathematics & Statistics
