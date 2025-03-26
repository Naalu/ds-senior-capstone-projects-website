## Introduction

### Description
Northern Arizona University Department of Mathematics & Statistics Research Showcase is dedicated to developing a web-based platform for Northern Arizona University's Department of Mathematics & Statistics. This platform aims to organize, archive, and showcase student research, particularly senior capstone projects, with potential expansions for additional research and other departments.

### Value Proposistion: 
For students, faculty, and external evaluators who need a reliable and structured platform to manage and discover research, the Mathematics & Statistics Research Showcase is a web-based academic repository that streamlines research submission, display, and discovery.

### Core Features (MVP)
✔ **Faculty-Driven Research Submission** – Faculty can submit student research with metadata (title, author, category, faculty advisor) and file uploads (PDF, PPT, images).

✔ ******Admin Review & Approval** – Admins can approve, reject, or request revisions before projects are published.

✔ **Advanced Search & Filtering** – Users can search by title, research category, faculty advisor, or keywords to find relevant projects.

✔ **Public Research Repository** – Approved projects are accessible to students, faculty, and external audiences.

✔ **Secure Role-Based Access Control** – Only faculty and admins can submit, review, and manage projects.

✔ **Efficient Research Management** – Admins manage research projects, user roles, and system settings through an intuitive Django Admin Panel.


Grading criteria (1 point): This section will be evaluated in terms of correctness, completeness, thoroughness, consistency, coherence, and adequate use of language. The description should be consistent with the current state of the project. You should include the link to GitHub.

## Requirements

List in this section, the requirements and associated pull request that you implemented for this release, following the example below---include the description of the requirement, a link to the issue, a link to the pull request(s) that implement the requirement, who implemented the requirement, who approved it, and a print screen that depicts the implemented feature (if applicable). I expect that you implement the features you specified in your MVP (c.f. D.2 Requirements). 

Order the requirements below by the name of the student who implemented them. All the members of the group should have worked on implementation activities and submitted pull requests. Only stable code should be included in the release. The code that is still under development should be in branches.

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
**Print screen**: [Insert screenshot showing role selection or admin interface]

### Requirement:
 As an administrator, I want to store capstone projects in a central location so that I can store and manage them more easily.

**Criteria:**

    - Focusing on Faculty and Admin roles
    - Enabling Faculty to submit research on behalf of students
    - Allowing Admins to access both submission and review features
    - Improving the permission system for more intuitive access control
    - Updating the documentation to reflect these changes including the README and usage guides for Faculty and Admins

**Issue(s):**
- [#51 - Create User Documentation](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/16)
- [#16 User Story 2](https://github.com/Naalu/ds-senior-capstone-projects-website/issues/16)

**Pull Request**: [#Y - Implement refined user roles](link-to-pull-request)  
**Implemented by**: Karl Reger  
**Approved by**: Jack Tomlon  
**Print screen**: [Insert screenshot showing role selection or admin interface]


Grading criteria (8 points): This section will be evaluated in terms of correctness, completeness, thoroughness, consistency, coherence, adequate use of language, and amount of work put into the implementation. Students can receive different grades depending on their involvement. It is expected that all members contribute with non-trivial implementation. All pull requests should be approved and integrated by the quality assurance person. You should follow an adequate workflow (description of the requirement on the issue tracker, submission of the implemented requirement as a pull request, and review of the pull request by another developer). 

## Tests

    You should implement automated tests that aim to verify the correct behavior of your code. Provide the following information:
    Test framework you used to develop your tests (e.g., JUnit, unittest, pytest, etc.)
    Link to your GitHub folder where your automated unit tests are located.
    An example of a test case. Include in your answer a GitHub link to the class being tested and to the test.
    A print screen showing the result of the execution of the automated tests. 

Django's built in testing system. In each Django module/app there is a test.py file for testing.

- https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/research/tests.py 

- https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/users/tests.py

[test screen shot]

Grading criteria (3 points): You should have an adequate number of automated tests. They should be well-written to exercise the main components of your system, covering the relevant inputs.

## Technology

Django is a popular choice for developing a project like the "ds-senior-capstone-projects-website" because of its benefits:

    Rapid Development: Django's built-in tools for routing, templating, and database management speed up development.

    Scalability: Django is well-suited for projects that might grow over time, such as expanding to accommodate more research departments.

    Built-in Admin Interface: Useful for managing research submissions and user roles without extra effort.

    Security: Django has built-in protection against common vulnerabilities like SQL injection, XSS, and CSRF.

    ORM (Object-Relational Mapping): Simplifies database interactions, ideal for handling structured data like student projects.

    Community Support: Extensive documentation and community resources make problem-solving easier.

Given the project's goals—to organize, archive, and showcase student research—Django's structure and capabilities are a strong fit.

## Deployment

Currently our project is being hosted locally but we have identified several cloud platforms that are suitable for hosting our project. The goal is to deploy the system in a cloud environment to improve its scalability, availability, and accessibility. If our project shows promise Northern Arizona University Department of Mathematics & Statistics may take over the project for further development and implementation.

Here are some cloud hosting platforms we discussed using:

    AWS(Amazon Web Service):
    AWS is one of the most popular cloud services used today. It offers feww credits for students, and the platform provides an array of tool and services. These include EC2 for virtucal servers, S3 for storage, and RDS for database management. AWS is ideal for larger, complex projects that may require high scalability and avaliablity.

    Microsoft Azure: 
    Azure is also a great alternative for web cloud service. Azure offers $100 in free credits and is free for students as well. They have Azure App Service for app hoting and Azure SQL Database for database management. Azure has integreation with Visual Studio which makes it an amazing choice for our project. Azure also supports automate deployment pipelines through CI/CD.

## Licensing

Inform the license you adopted for your source code (remember to configure GitHub accordingly). Explain why you adopted this license. For more information, check https://choosealicense.com/.

Grading criteria (1 point): This section will be evaluated in terms of correctness, completeness, thoroughness, consistency, coherence, and adequate use of language.

## Readme File

- [ReadMe](https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/README.md)  
- [Contributing ](https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/CONTRIBUTING.md) 
- [Code of Conduct](https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/CODE_OF_CONDUCT.md)
- [License](https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/LICENSE)

## UX Design

Describe the approach you adopted to design your user interface. Include some screenshots.

Grading criteria (3 points): This section will be graded based on the appearance (aesthetics) and usability (ease of use) of the system.

## Lessons Learned

In retrospective, describe what your team learned during this first release and what you are planning to change for the second release. 

Grading criteria (2 points): Adequate reflection about problems and solutions, clear description with adequate use of language. 

## Demo

Include a link to a video showing the system working.

Grading criteria (5 points): This section will be graded based on the quality of the video and on the evidence that the features are running as expected. Additional criteria are the relevance of the demonstrated functionalities, the correctness of the functionalities, and the quality of the developed system from the external point of view (user interface).
