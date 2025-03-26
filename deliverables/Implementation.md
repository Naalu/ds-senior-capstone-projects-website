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
**Print screen**:

![Requirement](images/admin-panel.png)  

## Tests 

We are using Django's built in testing system. In each Django module/app there is a test.py file for testing.

- https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/research/tests.py 

- https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/users/tests.py  

![Test Case Example](images/python_test_example.png)

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

Provide a link for the system in production and describe how you are deploying your system. 

Some alternatives for deploying your system in the cloud:

    AWS. AWS Educate offers free credits for students. See the tutorial at https://docker-curriculum.com/ on how to create a container and deploy it on AWS. 
    Digital Ocean or Azzure. As part of the GitHub Education benefits, as a student, you can get $100 at Digital Ocean and $100 at Microsoft Azzure cloud computing platforms (see more details at https://education.github.com/students) 

    Links to an external site..
    Oracle Cloud. Oracle offers a free tier in its cloud environment that should be more than enough for your needs.
    Firebase. Firebase can be a good choice if you are building a mobile phone app.

Grading criteria (3 points): This section will be graded based on the adequate use of the technology and its adequate description.

## Licensing

Inform the license you adopted for your source code (remember to configure GitHub accordingly). Explain why you adopted this license. For more information, check https://choosealicense.com/.

Grading criteria (1 point): This section will be evaluated in terms of correctness, completeness, thoroughness, consistency, coherence, and adequate use of language.

## Readme File

You should also prepare your repository for receiving new contributors. You should prepare a Readme.md file. See an example at https://gist.github.com/PurpleBooth/109311bb0361f32d87a2   In the Readme file, the current version should be stated. You should follow the Semantic Versioning schema (https://semver.org/). Tag the GitHub repository accordingly (https://git-scm.com/book/en/v2/Git-Basics-Tagging). 

Your repository should contain a CONTRIBUTING.md file, a LICENSE file, and a CODE_OF_CONDUCT.md file. Search online for some examples of these files. In this section of the deliverable, put links to these files on GitHub.

Grading criteria (3 points): This section will be based on the presence and quality of the information presented in the files.

## UX Design

Describe the approach you adopted to design your user interface. Include some screenshots.

Grading criteria (3 points): This section will be graded based on the appearance (aesthetics) and usability (ease of use) of the system.

## Lessons Learned

In retrospective, describe what your team learned during this first release and what you are planning to change for the second release. 

Grading criteria (2 points): Adequate reflection about problems and solutions, clear description with adequate use of language. 

## Demo

Include a link to a video showing the system working.

Grading criteria (5 points): This section will be graded based on the quality of the video and on the evidence that the features are running as expected. Additional criteria are the relevance of the demonstrated functionalities, the correctness of the functionalities, and the quality of the developed system from the external point of view (user interface).