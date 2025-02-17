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

# For Contributors

## Setting Up the Development Environment

Follow these steps to set up the local development environment for the **Data Science Senior Capstone Projects Website**.

### 1. Clone the Repository

First, clone the repository and navigate into the `research_showcase` directory:

```bash
git clone https://github.com/Naalu/ds-senior-capstone-projects-website.git
cd ds-senior-capstone-projects-website/research_showcase
```

---

### 2. Create and Activate a Virtual Environment

#### **macOS/Linux**
```bash
python -m venv venv
source venv/bin/activate
```

#### **Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Project Dependencies

Once the virtual environment is activated, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

If dependencies change, update them with:

```bash
pip install --upgrade -r requirements.txt
```

---

### 4. Apply Database Migrations

Run the following command to set up the database schema:

```bash
python manage.py migrate
```

If you encounter issues, you can reset the database with:

```bash
python manage.py flush
```

---

### 5. Create a Superuser (Optional)

If you need access to the Django Admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up a username, email, and password.

---

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Once running, access the project at:

- **Frontend:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### 7. Managing Static Files

To ensure static files (CSS, JS) are properly served:

```bash
python manage.py collectstatic --noinput
```

---

### 8. Loading Sample Data (Optional)

If test data is available, load it into the database:

```bash
python manage.py loaddata sample_data.json
```

---

### 🔧 Troubleshooting

- **Issue: `Command not found` for Python**
  - Use `python3` instead of `python`
  - Use `pip3` instead of `pip`

- **Issue: Missing Dependencies**
  - Run: `pip install --upgrade -r requirements.txt`

- **Issue: Database Errors**
  - Reset database with: `python manage.py flush`

- **Issue: Changes Not Reflected**
  - Restart server: `Ctrl + C` and re-run `python manage.py runserver`
  - Clear browser cache or try **private browsing mode**

---

### 🎯 Development Guidelines

- Ensure all new dependencies are added to `requirements.txt`
- Follow Django's **coding conventions** and **best practices**
- Use **feature branches** for development and open a **pull request** before merging into `main`
