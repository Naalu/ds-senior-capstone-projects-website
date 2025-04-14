# **NAU Research Showcase API Guide**

## Table of Contents

1. [API Documentation](#api-documentation)
   - [Submit Research Project](#submit-research-project)
   - [Review Research Project](#review-research-project)
   - [Approve Research Project](#approve-research-project)
   - [Reject Research Project](#reject-research-project)
   - [Search Research Projects](#search-research-project)

---

## **API Documentation**

### **Submit Research Project**
- **Description**: Submits a new research project.
- **Method**: POST
- **Request Body**:
  - `title`: (string) The title of the research project.
  - `abstract`: (string) A brief summary of the research.
  - `student_author_name`: (string) Name of the student researcher.
  - `collaborator_names`: (string) Text field listing all collaborators (separated by commas).
  - `faculty_advisor`: (integer) ID of the faculty advisor.
  - `github_link`: (string, optional) Link to the GitHub repository.
  - `project_sponsor`: (string, optional) The name of the project sponsor.
  - `poster_image`: (file, optional) Upload a poster image.
  - `video_link`: (string, optional) Link to an external video.
  - `presentation_file`: (file, optional) Upload a presentation file.
  - `pdf_file`: (file, optional) Upload a PDF file for the research paper.

- **Response**:
  - **200 OK**: If the submission is successful.
  - **400 Bad Request**: If required fields are missing or incorrect.


### **Review Research Project**
- **Description**: Allows admins to review submitted research projects.

- **Method**: POST

- **Request Body**:
    - `project_id`: (integer) The ID of the research project being reviewed.
    - `review_comments`: (string) Comments or feedback on the project.
    - `status`: (string) The review status (approved or rejected).

- **Response**:
    - **200 OK**: If the review is successfully submitted.
    - **400 Bad Request**: If required fields are missing or incorrect.



### **Approve Research Project**
- **Description**: Approves a research project.

- **Method**: POST

- **URL Parameters**:
    - `project_id`: (integer) The ID of the research project to approve.

- **Response**:

    - **200 OK**: If the research project is successfully approved.
    - **404 Not Found**: If the project ID does not exist.

### **Reject Research Project**
- **Description**: Rejects a research project with a provided reason.

- **Method**: POST

- **URL Parameters**:

    - `project_id`: (integer) The ID of the research project to reject.

- **Request Body**:

    - `rejection_reason`: (string) Reason for rejecting the project.

- **Response**:

    - **200 OK**: If the research project is successfully rejected.

    - **404 Not Found**: If the project ID does not exist.


### **Search Research Project**
 - **Description**: Searches for research projects by title, abstract, or project sponsor.

- **Method**: GET

- **Query Parameters**:

    - `q`: (string, optional) Search query (e.g., title, abstract, or project sponsor).

    - `start_semester`: (string, optional) The starting semester (e.g., "Fall 2024").

    - `end_semester`: (string, optional) The ending semester (e.g., "Spring 2025").

- **Response**:

    - **200 OK**: Returns the list of filtered research projects based on the search query and date range.

     - **404 Not Found**: If no results match the search.

## Need Help?

- **Use the Help button** in the application navigation
- **Contact the system administrator** through the contact form
- **Report technical issues** via the feedback option
