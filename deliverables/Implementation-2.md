## Introduction

### Description
Northern Arizona University Department of Mathematics & Statistics Research Showcase is dedicated to developing a web-based platform for Northern Arizona University's Department of Mathematics & Statistics. This platform aims to organize, archive, and showcase student research, particularly senior capstone projects, with potential expansions for additional research and other departments.

[GitHub Link](https://github.com/Naalu/ds-senior-capstone-projects-website)

### Value Proposistion: 
For students, faculty, and external evaluators who need a reliable and structured platform to manage and discover research, the Mathematics & Statistics Research Showcase is a web-based academic repository that streamlines research submission, display, and discovery.

### Core Features (MVP)
✔ **Faculty-Driven Research Submission** – Faculty can submit student research with metadata (title, author, category, faculty advisor) and file uploads (PDF, PPT, images).

✔ **Admin Review & Approval** – Admins can approve, reject, or request revisions before projects are published.

✔ **Advanced Search & Filtering** – Users can search by title, research category, faculty advisor, or keywords to find relevant projects.

✔ **Public Research Repository** – Approved projects are accessible to students, faculty, and external audiences.

✔ **Secure Role-Based Access Control** – Only faculty and admins can submit, review, and manage projects.

✔ **Efficient Research Management** – Admins manage research projects, user roles, and system settings through an intuitive Django Admin Panel.

## Requirements

### EXAMPLE

### Requirement:
As a student, I want to my capstone project stored online so that I can share my work with others in the department and prospective employers.

**Criteria:**

    Functionality for documents (PDF, LaTeX) and supplementary files (data sets, code, etc.).
    Ability to add a project title, description, and keywords.
    Option to tag faculty or collaborators related to the project.

**Issue(s):**  
 -[ User story 1 ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/15)  
 -[ Create comprehensive sample data ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/44)

**Pull Request**: [#Y - Implement refined user roles](link-to-pull-request)    
**Implemented by**: Jack Tomlon  
**Approved by**: Karl Reager   
**Print screen**: Back-end no availiable screenshot.  


# // PLACE NEW DEVELOPMENTS HERE


### Requirement:
As a faculty member, I want to browse through capstone projects so that I can review student work and provide feedback.

**Criteria:**

    Search and filter options for browsing projects by topic, student name, year, and keywords.
    Preview of project summaries and a link to view detailed information.
    Access to provide feedback or comments for each project.

**Issue(s):**  
 -[ User story 9 ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/23)  
 -[ User story 6 ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/20)  
 -[ Rylan begins development ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/4)
 -[ Implement search and filtering system ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/40)

**Pull Request**: [#65 - Date Range Search](https://github.com/Naalu/ds-senior-capstone-projects-website/pull/65)    
**Implemented by**: Rylan Harris  
**Approved by**:  Chris Reger
**Print screen**: ![Date Range Image](images\date-range.png)

### Requirement:
As a student, I want to my capstone project stored online so that I can share my work with others in the department and prospective employers.

Enhance research submission form #38

**Criteria:**

    The current research submission form needs improvements for better usability and data validation.  

    Implemented: Validation for Github and video links

**Issue(s):**  
 -[ User story 1 ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/15)  
-[ issue 38 ](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/38)

**Pull Request**: [#Y - Implement link validations](https://github.com/Naalu/ds-senior-capstone-projects-website/pull/67)    
**Implemented by**: Jack Tomlon  
**Approved by**:  
**Print screen**: 
![Date Range Image](images\Enter_valid_link_error.png)
![Date Range Image](images\Video_link_Error.png)


## Tests

Django's built in testing system. In each Django module/app there is a test.py file for testing.

- https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/research/tests.py 

- https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/users/tests.py  

![Test Case](images/python_test_example.png)  

## Technology

Django is a popular choice for developing a project like the "ds-senior-capstone-projects-website" because of its benefits:

    Rapid Development: Django's built-in tools for routing, templating, and database management speed up development.

    Scalability: Django is well-suited for projects that might grow over time, such as expanding to accommodate more research departments.

    Built-in Admin Interface: Useful for managing research submissions and user roles without extra effort.

    Security: Django has built-in protection against common vulnerabilities like SQL injection, XSS, and CSRF.

    ORM (Object-Relational Mapping): Simplifies database interactions, ideal for handling structured data like student projects.

    Community Support: Extensive documentation and community resources make problem-solving easier.

Given the project's goals—to organize, archive, and showcase student research—Django's structure and capabilities are a strong fit.

## Demo

# // NEED NEW DEMO VIDEO

[Demo video zoom link]() 

## Code Quality

    Describe how your team managed code quality. What were your policies, conventions, adopted best practices, etc. to foster high-quality code?  

    Grading criteria (4 points): Adequate list of practices that were adopted to improve code quality and clear description with adequate use of language.

## Lessons Learned

    In retrospect, describe what your team learned during this second release and what would you change if you would continue developing the project.   

    Grading criteria (2 points): Adequate reflection about problems and solutions, clear description with adequate use of language.



