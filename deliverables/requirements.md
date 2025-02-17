# Requirements

Team 14

## Team Members

- Ethan Ferguson
- Jack Tomlon
- Karl Reger
- Rylan Harris-Small

## 1. Positioning

### Problem statement

*The problem of* **the lack of a centralized, structured platform for storing and showcasing Mathematics and Statistics student research** *affects* **students, faculty, and external evaluators (such as employers, graduate programs, and** **prospective students**), *the impact of which is* **diminished research visibility, ineffective knowledge-sharing, and lost academic and professional opportunities**.

Without an organized system, students struggle to showcase their work, faculty lack an easy way to reference past research, and external audiences find it difficult to evaluate the department’s academic output.

### Product Position Statement

*For* **students, faculty, and external evaluators** *who* **need a reliable and structured platform to manage and discover research**, t*he* **Mathematics & Statistics Research Showcase** *is a* **web-based academic repository** *that* **streamlines research submission, display, and discovery.** *Unlike* **current** **ad hoc solutions like GitHub or departmental posters, which lack centralized organization and faculty oversight**, *our product* **offers a seamless submission workflow, faculty moderation, and an intuitive, searchable archive for student research projects, effectively enhancing visibility and accessibility for all stakeholders**.

### Value Proposition

The **Mathematics & Statistics Research Showcase** is a **web-based research repository** that allows **students and faculty in the Mathematics & Statistics Department** to **store, organize, and showcase student research in a structured and searchable format,** eliminating **fragmented storage, increasing visibility for students, and providing faculty with an efficient research archive**.

### Customer Segment

1. **Students** with no structured way to showcase research for grad schools and employers.
2. **Faculty** with no centralized database for referencing past projects or advising students.
3. **External Evaluators (employers, graduate schools, prospective students)** lacking an easy way to assess student work in the department.

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

- **Description:** Administrative staff responsible for maintaining and overseeing the platform’s operations.

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

## 3. Functional Requirements (features)

1. **Faculty Registration & Authentication**
    1. Faculty must securely log in using university credentials or email authentication.
2. **Role-Based Access Control (RBAC)**
    1. Faculty can submit research and manage their own past submissions.
    2. Admins can approve or reject research, manage users, and adjust system settings.
3. **Faculty Research Submission Portal**
    1. Faculty must be able to submit research projects on behalf of students by entering:
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

o   Their research is approved or requires revision.

o   Admins must receive notifications when:

o   A new research submission is pending review.

11.  External Research Sharing

o   The system must allow users to generate shareable links for research projects.

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

7. **Accessibility (ISO-IEC: Usability → Accessibility)**

    1. **Significance:** Faculty and admins with disabilities must be able to use the system without barriers.

    2. **Verifiability:**

        1. The platform must comply with **WCAG 2.1 AA accessibility standards** (e.g., keyboard navigation, screen reader support).

        2. All interactive elements must be **navigable via keyboard shortcuts** without requiring a mouse.

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

## 6. Use cases

- Include a UML use case diagram for your project. There are many drawing tools that you can use. I recommend the one we used in class, draw.io.

Grading criteria (5 points): Follow correctly the UML specification. The actors should be coherent with what was listed in sections 1 and 2. The use case diagram should be coherent with the list of requirements (section 3). The level of granularity of each use case should be adequate. The use cases should be adequately named.

Present one complete use case description (textual) for each member of the group. Therefore, if the group has 4 members, 4 use case descriptions are necessary. As the grading will not be individual, the group is responsible for keeping the quality and consistency of the whole document – avoid just splitting the work. Choose the most important use cases to describe. Follow the template provided in the slides.

After each use case description, add a sketch of the corresponding user interface. This will be a good opportunity to start thinking about usability.

Grading criteria (8 points): Follow the template to describe the use cases. Present an interface sketch for each use case. Describe the use case as a dialog between the user and the system. Do not use UI language in the description of the use case.

## 7. User stories

Write two user stories for each member of the group. They can be related to the same features described in the use cases or to different ones. Adopt the following format: "As a <ROLE>, I want <SOMETHING> so that <GOAL>."

Establish a priority level for each user story and estimate how many hours each one will demand using the planning poker approach.

Grading criteria (6 points): Use the provided format. The user stories should be in an adequate level of granularity (not too broad nor too specific). Provide the priority and estimation for each user story.

## 8. Issue Tracker

The user stories should be registered in your GitHub issue tracker. Include here the link for your issue tracker and a screenshot of what you did.

Grading criteria (1 point): Provide the URL and screenshot of the issue tracker. The user stories should be registered there.

Format Your document should be composed in Markdown and hosted on GitHub but you should also turn in a PDF copy to be graded. See also Converting GitHub Markdown to PDF. Sections should use appropriate markdown and figures should be included if needed or appropriate.

Teamwork The contribution of each team member may be different but we expect the amount of work to be roughly even. When you submit the deliverable, the person submitting the deliverable should describe what each member worked on and a rough percentage estimation of their contribution as a submission comment. Here's an example:

John Doe (40%) – Conducted 2 interviews, wrote section 2.3, and reviewed the whole document. Mary Shawn (40%) – Conducted 1 interview, wrote sections 1 and 2.1, reviewed section 2.3, and worked on the source code. Lucy Johnson (20%) – Wrote section 2.2 and performed code review. We will also be reviewing your github repository, which should also reflect the work happening in your team. Every team member should be committing and making meaningful contributions in your repository.

Individual grades may be reduced based on a combination of what we see in the deliverable summary and github contributions. If there's no evidence that a team member contributed to the deliverable, they should absolutely expect to receive a zero!
