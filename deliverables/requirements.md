# Requirements

Team 14

## Team Members

- Ethan Ferguson
- Jack Tomlon
- Karl Reger
- Rylan Harris-Small

------------------------------------------------------------------------

## 1. Positioning

### Problem statement

*The problem of* **the lack of a centralized, structured platform for storing and showcasing Mathematics and Statistics student research** *affects* **students, faculty, and external evaluators (such as employers, graduate programs, and** **prospective students**), *the impact of which is* **diminished research visibility, ineffective knowledge-sharing, and lost academic and professional opportunities**.

Without an organized system, students struggle to showcase their work, faculty lack an easy way to reference past research, and external audiences find it difficult to evaluate the department's academic output.

### Product Position Statement

*For* **students, faculty, and external evaluators** *who* **need a reliable and structured platform to manage and discover research**, t*he* **Mathematics & Statistics Research Showcase** *is a* **web-based academic repository** *that* **streamlines research submission, display, and discovery.** *Unlike* **current** **ad hoc solutions like GitHub or departmental posters, which lack centralized organization and faculty oversight**, *our product* **offers a seamless submission workflow, faculty moderation, and an intuitive, searchable archive for student research projects, effectively enhancing visibility and accessibility for all stakeholders**.

### Value Proposition

The **Mathematics & Statistics Research Showcase** is a **web-based research repository** that allows **students and faculty in the Mathematics & Statistics Department** to **store, organize, and showcase student research in a structured and searchable format,** eliminating **fragmented storage, increasing visibility for students, and providing faculty with an efficient research archive**.

### Customer Segment

1. **Students** with no structured way to showcase research for grad schools and employers.
2. **Faculty** with no centralized database for referencing past projects or advising students.
3. **External Evaluators (employers, graduate schools, prospective students)** lacking an easy way to assess student work in the department.

------------------------------------------------------------------------

## 2. Stakeholders

**Primary Stakeholders (Direct Users of the System)**

**1. Students** (Primary Users & Research Submitters)

- **Description:** Students in the Mathematics & Statistics department seeking a platform to showcase their research projects.

- **Responsibilities:**

  - Submit research projects, including papers, posters, and presentations.

  - Browse and reference previous student work for academic and professional purposes.

  - Use the platform as a portfolio for job and graduate school applications.

**2. Faculty** (Research Moderators & Reviewers)

- **Description:** Faculty members supervising student research and ensuring submission quality.

- **Responsibilities:**

  - Review and approve student research prior to publication.

  - Reference archived research for advising and instructional purposes.

  - Curate high-quality submissions to highlight departmental research excellence.

**3. Department Administrators** (Platform Managers)

- **Description:** Administrative staff responsible for maintaining and overseeing the platform's operations.

- **Responsibilities:**

  - Enforce submission guidelines and ensure research meets departmental standards.

  - Manage system access, account permissions, and data integrity.

  - Assist faculty and students in effectively using the system.

**Secondary Stakeholders (Indirect Beneficiaries of the System)**

**4. External Evaluators** (Employers, Graduate Schools, Prospective Students)

- **Description:** Organizations and individuals assessing the quality of student research for hiring, graduate admissions, or academic benchmarking.

**Responsibilities:**

- Browse and review student research projects using structured search tools.

- Evaluate research credibility based on faculty approval and project details.

**5. Developers & Technical Team** (System Builders & Maintainers)

- **Description:** The technical team responsible for developing and maintaining the platform.

**Responsibilities:**

- Implement core system functionalities, including search, submission workflows, and authentication.

- Ensure system stability, security, and performance.

- Address bugs and continuously improve the user experience.

------------------------------------------------------------------------

## 3. Functional Requirements (features)

1. **Faculty Registration & Authentication**
    1. Faculty must securely log in using university credentials or email authentication.
2. **Role-Based Access Control (RBAC)**
    1. Faculty can submit student research and manage their own past submissions.
    2. Admins can approve or reject research, manage users, and adjust system settings.
3. **Faculty Research Submission Portal**
    1. Faculty must be able to submit student research projects by entering:
        1. Project title, student author(s), research category, faculty advisor, and attached files (PDFs, images, presentations).
4. **Admin Approval Workflow**
    1. Admins must be able to review the research submitted by faculty and:
        1. *Approve* (publishes the research in the system).
        2. *Request* revisions (faculty receives a notification to update).
        3. *Reject* (removes the submission).
5. **Search & Filtering System**
    1. Users (faculty, admins, and external visitors) must be able to search for projects using:
        1. Keywords, research category, faculty advisor, date, and file type.
6. **Project Browsing & Detailed View**
    1. Visitors (external users, faculty, and students) must be able to browse and view approved research projects.
7. **File Management & Storage**
    1. The system must support uploads of PDF, PowerPoint, and image files with a maximum file size of 50MB per file.
8. **Project Categorization & Metadata**
    1. Faculty must be able to categorize submissions using predefined tags (e.g., Machine Learning, Applied Statistics, Probability).
9. **Admin Dashboard**
    1. Admins must be able to:
        1. View all pending submissions.
        2. Approve, reject, or request revisions for research.
        3. Manage faculty accounts and system settings.
10. **User Notifications**
    1. Faculty must receive notifications when:
        1. Their research is approved or requires revision.
    2. Admins must receive notifications when:
        1. A new research submission is pending review.
11. **External Research Sharing**
    1. The system must allow users to generate shareable links for research projects.

------------------------------------------------------------------------

## 4. Non-Functional Requirements

1. **Usability (ISO-IEC: Usability → Learnability & Operability)**

    1. **Significance:** Faculty members with varying levels of technical expertise must be able to submit and manage research effortlessly.

    2. **Verifiability:**

        1. **Learnability** – Faculty should be able to submit a research project in **under 5 minutes** without requiring external guidance.

        2. **Operability** – All core tasks (submission, approval, browsing) should be **completed in 3 clicks or fewer** from the homepage.

2. **Performance Efficiency (ISO-IEC: Performance Efficiency → Time Behavior & Resource Utilization)**

    1. **Significance:** The system must be fast and responsive to support seamless research submissions, browsing, and approvals.

    2. **Verifiability:**

        1. **Time Behavior** – Page loads for research browsing and submission must complete in **under 2 seconds** for 95% of users.

        2. **Resource Utilization** – The system must maintain consistent performance with **at least 100 concurrent users accessing the platform**.

3. **Security (ISO-IEC: Security → Confidentiality, Integrity, & Authentication)**

    1. **Significance:** Since faculty submit research and admins approve it, access control must be strict, ensuring that unauthorized users cannot modify or delete research.

    2. **Verifiability:**

        1. **Authentication** – All users must log in with **hashed passwords (bcrypt or equivalent)** and use **role-based access control (RBAC)**.

        2. **Confidentiality** – Only **faculty and admins can log in**; research must not be accessible to unauthorized users before approval.

        3. **Integrity** – Once approved, research submissions must be **immutable unless explicitly modified by an admin**.

4. **Maintainability (ISO-IEC: Maintainability → Modularity & Modifiability)**

    1. **Significance:** The platform must support future enhancements, such as bulk uploads, new research categories, or external API integrations.

    2. **Verifiability:**

        1. **Modularity** – The system must follow a **modular architecture**, allowing new features to be implemented with **minimal code changes to existing components**.

        2. **Modifiability** – Code updates should not require more than **20% modification to the existing codebase for a new feature**.

5. **Availability (ISO-IEC: Availability → Fault Tolerance & Recoverability)**

    1. **Significance:** The platform must remain accessible to faculty and admins without unexpected downtime.

    2. **Verifiability:**

        1. **Fault Tolerance** – The system should **continue functioning normally** even if **one non-essential service (e.g., notifications) fails**.

        2. **Recoverability** – In case of failure, data recovery must be possible **within 24 hours** using system backups.

6. **Compatibility (ISO-IEC: Compatibility → Interoperability & User Environment Adaptability)**

    1. **Significance:** The system must function seamlessly across different browsers and devices, ensuring accessibility.

    2. **Verifiability:**

        1. **Interoperability** – The platform must support modern web browsers **(Chrome, Firefox, Edge)** without UI breakage.

        2. **User Environment Adaptability** – The platform must be **fully functional on mobile devices** without requiring additional software.

**Accessibility (ISO-IEC: Usability → Accessibility)**

1. **Significance:** Faculty and admins with disabilities must be able to use the system without barriers.

2. **Verifiability:**

    1. The platform must comply with **WCAG 2.1 AA accessibility standards** (e.g., keyboard navigation, screen reader support).

    2. All interactive elements must be **navigable via keyboard shortcuts** without requiring a mouse.

------------------------------------------------------------------------

## 5. Minimum Viable Product

### **Definition of the MVP**

The Mathematics & Statistics Research Showcase MVP will enable faculty to submit student research, allow administrators to review and publish projects, and create a searchable research repository. The focus is on streamlining the submission, approval, and discovery of research while ensuring usability, security, and accessibility.

### **Essential MVP Features**

#### Faculty Authentication & Role-Based Access Control (RBAC)

- Faculty can log in using their university credentials or email authentication.

- Administrators possess specific permissions for reviewing and approving research.

#### Faculty Research Submission Portal

- Faculty can submit research on behalf of students by providing the title, student author(s), research category, faculty advisor, and file attachments (PDF, PPT, images).

#### Admin Review & Approval Workflow

- Administrators can approve, request revisions, or reject research submissions.

- Faculty receive automated notifications regarding approvals or revision requests.

#### Research Browsing & Viewing

- Users can browse approved research projects organized by research area, faculty advisor, and keywords.

#### Search & Filtering System

- Users can search for projects by title, research category, faculty advisor, and keywords.

### MVP Validation Strategy

#### Faculty Authentication & Role-Based Access Control

- Validation: Test authentication processes for faculty and administrative roles.

- Success Criteria: Faculty and administrators can **log in** **within 10 seconds**, and unauthorized users **cannot access restricted features**.

#### Faculty Research Submission Portal

- Validation: Faculty complete test submissions under real-world conditions.

- Success Criteria: Faculty **submit** research in **5 minutes or less**, including all necessary metadata and attachments.

#### Admin Review & Approval Workflow

- Validation: Administrators review and either approve or reject test submissions.

- Success Criteria: Administrators can **approve or reject** research in **3 minutes or less**.

#### Research Browsing & Viewing

- Validation: Users navigate and browse published research projects.

- Success Criteria: Users can **access and view** a research project **within 5 clicks** from the homepage.

#### Search & Filtering System

- Validation: Users conduct targeted searches using various filter combinations.

- Success Criteria: Searches **return relevant results in 3 seconds or less for \>90% of queries**.

------------------------------------------------------------------------

## 6. Use cases

![use case diagram](images/UseCase.drawio.svg)

Use Case 1: *Submit Research*

Actor: Faculty

Trigger: Faculty decides to submit a student research project.

Pre-conditions: Faculty is logged in.

Post-condition: Student research submission is recorded and pending admin review.

Success Scenario:

1. Faculty provides student research details (title, studentauthor(s), research category, and faculty advisor).
2. The faculty uploads the research file(s), which may include PDFs, presentations, or images.
3. The system validates the submission and stores the files.
4. The system marks the research as "Pending Review."
5. The system notifies admins that a new research submission is awaiting approval.

Alternate Scenario:

1. The system detects an invalid file format or missing information.
2. The system informs the faculty of the issue and requests corrections.
3. The faculty resubmits the corrected student research.

![use case diagram](images/UseCase1.svg)

Use Case 2: *Approve/Reject Research*

Actor: Admin

Trigger: Admin decides to review a submitted research project.

Pre-conditions: Admin is logged in, and research submission is pending.

Post-condition: The research is either approved (published) or rejected (removed from the review queue).

Success Scenario:

1. Admin selects a pending research submission.
2. Admin reviews the research details and attached file.
3. Admin decides to approve the research.
4. The system marks the research as "Approved" and moves it to public access.
5. The system notifies faculty that their research has been approved.

Alternate Scenario:

3. Admin rejects the submission due to poor quality or policy violations.
4. The system marks the submission as "Rejected."
5. The system notifies faculty that the submission has been rejected.

![use case diagram](images/UseCase2.svg)

Use Case 3: *Browse Research*

Actor: Faculty, Admins, Visitors

Trigger: A user wants to explore published research projects.

Pre-conditions: The system has approved research projects.

Post-condition: The user successfully views research project details.

Success Scenario:

1. The user accesses the research repository.
2. The system presents a list of published research projects.
3. The user selects a research project to view details.
4. The system displays the research title, student author(s), faculty advisor, and attached files.

Alternate Scenario:

2. No research projects are available.
3. The system informs the user that no research has been published yet.

![use case diagram](images/UseCase3.svg)

Use Case 4: *Search Research*

Actor: Faculty, Admins, Visitors

Trigger: A user wants to find specific research.

Pre-conditions: Approved research projects exist in the system.

Post-condition: The user successfully retrieves relevant research results.

Success Scenario:

1. A user enters a search query (keywords, faculty advisor, category).
2. The system retrieves relevant research projects based on search criteria.
3. The system displays matching results.
4. The user selects a project from the results.
5. The system presents the research details and attached files.

Alternate Scenario:

3. No matching results are found.
4. The system informs the user that no projects match the search criteria.

![use case diagram](images/UseCase4.svg)

## 7. User Stories

1. *As a Math and Stats Professor, I want to store capstone projects in a central location so that I can reference and store them more easily.*

    **Priority:** High

    **Effort Estimate:** 6 hours

2. *As a website administrator, I want to have a website that lets me update the capstone repository so that I don't have to manually edit html and file structures to keep it up to date.*

    **Priority:** Medium

    **Effort Estimate:** 6 hours

3. *As a data science student, I want to browse past data science capstones so that I can get a better idea of what to do for my own.*

    **Priority:** High

    **Effort Estimate:** 12 Hours

4. *As a company, I want look through capstone projects so that I can see if I want to propose a research project collaboration with the department.*

    **Priority:** Low

    **Effort Estimate:** 12 Hours

5. *As a faculty member, I want to submit research on behalf of students so that their work can be officially archived and showcased.*

    **Priority:** Medium

    **Effort Estimate:** 6 hours

6. *As an admin, I want to review research submissions and approve or reject them so that only high-quality work is published.*

    **Priority:** Medium

    **Effort Estimate:** 6 hours

7. *As a faculty member, I want to receive notifications about student research I've submitted so that I know when it is approved or requires revisions.*

    **Priority:** Low

    **Effort Estimate:** 12 hours

8. *As an admin, I want to request revisions on submitted research so that faculty can improve the quality before approval.*

    **Priority:** Medium

    **Effort Estimate:** 12 hours

9. *As a visitor, I want to search for research using keywords, faculty names, and categories so that I can quickly find relevant projects.*

    **Priority:** High

    **Effort Estimate:** 24 hours

------------------------------------------------------------------------

## 8. Issue Tracker

<https://github.com/Naalu/ds-senior-capstone-projects-website/issues>

![use case diagram](images/issue_tracker.png)

------------------------------------------------------------------------

## Teamwork

- Ethan Ferguson (5%)
- Jack Tomlon (5%)
- Karl Reger (70%)
- Rylan Harris-Small (20%)
