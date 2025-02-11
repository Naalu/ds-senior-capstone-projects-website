# Northern Arizona University Department of Mathematics & Statistics Research Showcase Website

## **Project Overview**  

The **NAU Mathematics & Statistics Research Showcase** is a web-based platform designed to **archive, organize, and showcase** student research within **Northern Arizona University’s Department of Mathematics and Statistics**. Initially focused on **Senior Capstone projects**, this system will provide a **structured and accessible repository** for students, faculty, and external audiences such as employers and graduate programs.  

### **Key Objectives**  

- **Enhance Research Visibility** – Give students a professional space to **showcase** their research.  
- **Support Faculty & Academic Growth** – Provide a **searchable** database for faculty and students to reference past projects.  
- **Improve Accessibility & Usability** – Ensure research materials (including PDFs, abstracts, and presentations) are easily searchable and well-organized.  
- **Expand Opportunities** – Allow external audiences, including **graduate schools, employers, and prospective students**, to explore NAU’s research contributions.  
- **Scale for the Future** – Built with **Django & SQLite3**, the system is designed for **future expansions** to include additional research projects, interdisciplinary collaborations, and more departments at NAU.  

### **Core Features (MVP)**  

✔️ **Student Research Submission System** – Students submit capstone projects, including abstracts, PDFs, and presentations.  
✔️ **Faculty Approval Workflow** – Faculty can review, approve, or request revisions before publishing projects.  
✔️ **Search & Filtering** – Users can browse projects by **title, author, advisor, research topic, or date**.  
✔️ **Secure User Authentication** – Students, faculty, and admins have role-based permissions for submission and approval.  
✔️ **Django Admin Panel** – Faculty and admins can manage research projects efficiently.  

### **Future Enhancements**  

- **Colloquium & Seminar Archive** – Store and display department seminars and research presentations.  
- **Project Highlights & Awards** – Feature outstanding student research projects.  
- **Multi-Department Expansion** – Allow other departments at NAU to contribute.  

---

## **Why This Project Matters**  

Currently, NAU **does not have a centralized system** for showcasing student research, making it difficult for:  

- Students to **share their work with employers or graduate schools**.  
- Faculty to **reference past projects** for advising and curriculum improvement.  
- External audiences to **evaluate NAU’s research contributions**.  

By providing a **well-structured and accessible platform**, this project aims to **bridge these gaps** while **modernizing** how student research is documented and shared.

***

## Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone <GITHUB_REPO_URL>
   cd research_showcase
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows, use venv\Scripts\activate
   ```

3. Install the required project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Clone the Repository and Set Up the Development Environment

```bash
   git clone https://github.com/Naalu/ds-senior-capstone-projects-website.git
   cd research_showcase
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
```
