# **Northern Arizona University Department of Mathematics & Statistics Research Showcase**  

## **Overview**  

The **NAU Mathematics & Statistics Research Showcase** is a **web-based platform** designed to **organize, archive, and showcase** student research within **Northern Arizona University’s Department of Mathematics & Statistics**.  

This system provides a **structured, searchable repository** where **faculty submit student research**, and **admins approve and publish projects**. It ensures increased **visibility for students**, facilitates **academic reference for faculty**, and allows **external audiences such as employers and graduate schools** to explore NAU’s research contributions.  

---

## **Key Objectives**  

✅ **Increase Research Visibility** – Provide a **dedicated, accessible platform** to showcase student research.  
✅ **Improve Academic Accessibility** – Organize research materials (PDFs, abstracts, presentations) in a **searchable, structured repository**.  
✅ **Support Faculty & Curriculum Development** – Help faculty **reference past projects** for advising, curriculum improvements, and research collaboration.  
✅ **Expand Career & Academic Opportunities** – Enable **graduate schools, employers, and prospective students** to explore NAU’s research.  
✅ **Ensure Long-Term Scalability** – Built with **Django & SQLite3**, the platform is designed for **future expansion** across disciplines.  

---

## **Core Features (MVP)**  

✔ **Faculty-Driven Research Submission** – Faculty can submit student research with **metadata (title, author, category, faculty advisor) and file uploads (PDF, PPT, images).**  
✔ **Admin Review & Approval** – Admins can **approve, reject, or request revisions** before projects are published.  
✔ **Advanced Search & Filtering** – Users can search by **title, research category, faculty advisor, or keywords** to find relevant projects.  
✔ **Public Research Repository** – Approved projects are **accessible to students, faculty, and external audiences**.  
✔ **Secure Role-Based Access Control** – Only **faculty and admins** can submit, review, and manage projects.  
✔ **Efficient Research Management** – Admins manage **research projects, user roles, and system settings** through an intuitive **Django Admin Panel**.  

---

## **Future Enhancements**  

🔹 **Colloquium & Seminar Archive** – Store and display **research presentations & departmental seminars**.  
🔹 **Featured Research & Awards** – Highlight **outstanding student research projects**.  
🔹 **Cross-Disciplinary Expansion** – Allow **other NAU departments** to contribute research.  
🔹 **External Integrations** – Enable **faculty to link projects to Google Scholar, LinkedIn, or ORCID profiles**.  

---

## **Why This Project Matters**  

The department currently **lacks a centralized system** for showcasing student research, making it difficult for:  

🔹 **Students** – To share their work with **employers or graduate programs**.  
🔹 **Faculty** – To reference past research for **advising, teaching, and collaboration**.  
🔹 **External Audiences** – To explore **NAU’s research contributions and student work**.  

By creating a **structured, user-friendly, and publicly accessible platform**, this project **modernizes** how the department documents, manages, and shares student research, ensuring long-term **academic and professional benefits**.  

---

## **Why This Project Matters**  

Currently, NAU **does not have a centralized system** for showcasing student research, making it difficult for:  

- Students to **share their work with employers or graduate schools**.  
- Faculty to **reference past projects** for advising and curriculum improvement.  
- External audiences to **evaluate the department’s research contributions**.  

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
