# Analysis

Group 14

## Team Members

- Ethan Ferguson
- Jack Tomlon
- Karl Reger
- Rylan Harris-Small

## System Description

The **NAU Mathematics & Statistics Research Showcase** addresses *the problem* of the lack of a centralized, structured platform for storing and showcasing Mathematics and Statistics student research, which affects **students**, **faculty**, and **external evaluators** such as employers, graduate programs, and prospective students. The impact is diminished research visibility, ineffective knowledge-sharing, and lost academic and professional opportunities. For students, faculty, and external evaluators who need a reliable and structured platform to manage and discover research, the **Mathematics & Statistics Research Showcase** is a web-based academic repository that streamlines research submission, display, and discovery. Unlike current ad hoc solutions like GitHub or departmental posters, which lack centralized organization and faculty oversight, our product offers a seamless submission workflow, faculty moderation, and an intuitive, searchable archive for student research projects.

The core functionality centers around the **Faculty** role, where faculty members ***submit*** **ResearchProject** entries on behalf of students. Each **ResearchProject** contains essential *attributes* including *title*, *abstract*, *submission_date*, and *approval_status*. Faculty can also include optional elements such as *github_link*, *project_sponsor*, *poster_image*, *video_link*, *presentation_file*, and *pdf_file* to enhance the research presentation. A **User** with the faculty role not only ***submits*** **ResearchProject** entries but can also be ***associated with*** projects as ***collaborators*** or serve as a ***faculty_advisor***. The system additionally manages **Colloquium** events with *title*, *date*, *description*, and optional *video_link* and *presentation_file* attributes, where a **User** ***presents*** a **Colloquium**.

The **Admin** role is critical for quality control, as administrators ***review*** and ***approve*** or ***reject*** submitted research through a structured workflow. When a **Faculty** member submits a **ResearchProject**, its *approval_status* is set to "pending." An **Admin** then reviews the submission and changes the *approval_status* to either "approved" or "rejected." The system implements role-based access control through the **User** class, which contains a *role* attribute that determines permissions. Only users with the *faculty* role can submit research, while only those with the *admin* role can approve or reject submissions.

**Visitors**, including students, faculty, and external evaluators, can ***browse*** and ***search*** the repository of approved research. The system features comprehensive search and filtering capabilities allowing users to find research based on titles, research categories, faculty advisors, and keywords. This makes the platform valuable for students seeking examples for their own work, faculty referencing past projects, and external parties evaluating the department's research output. All approved research is publicly accessible through an intuitive browsing interface that displays project details in a structured format.

The architecture prioritizes security, usability, and maintainability. Authentication ensures that only authorized **Users** can perform role-specific actions, while the public-facing components remain accessible to all **Visitors**. The modular design supports future expansion to include features such as featured research sections, cross-disciplinary integration, and external platform connections. This approach ensures the system can evolve while continuing to serve its primary purpose of enhancing research visibility and accessibility for all stakeholders.

## Model

![UML Model](images/Analysis-UML.drawio.svg)
