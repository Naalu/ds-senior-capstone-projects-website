# Description

Northern Arizona University Department of Mathematics & Statistics Research Showcase is dedicated to developing a web-based platform for Northern Arizona University's Department of Mathematics & Statistics. This platform aims to organize, archive, and showcase student research, particularly senior capstone projects, with potential expansions for additional research and other departments.

## Verification

This section demonstrates how we ensured that the project was developed properly using a robust testing strategy.

### Test Framework

The automated tests for the NAU Research Showcase were developed using **Django's built-in testing framework**. This framework is based on Python's standard `unittest` module and provides specialized tools for testing Django applications, including:

- `django.test.TestCase`: A subclass of `unittest.TestCase` that manages database setup/teardown per test and offers Django-specific assertions.
- `django.test.Client`: A test client for simulating HTTP requests (GET, POST) to test views without a live server.
- `unittest.mock.patch`: A decorator/context manager from Python's standard library, integrated seamlessly with Django's test runner, used for isolating components by replacing dependencies with mock objects during tests.

This framework was chosen because it integrates directly with the Django project structure, simplifies database interactions in tests, and provides convenient utilities for testing web application features like views, forms, and models.

### Automated Tests Location

The automated unit and integration tests are located within the `tests` directory inside each respective Django application folder:

- **Research App Tests:** [research_showcase/research/tests/](https://github.com/Naalu/ds-senior-capstone-projects-website/tree/main/research_showcase/research/tests)
- **Users App Tests:** [research_showcase/users/tests/](https://github.com/Naalu/ds-senior-capstone-projects-website/tree/main/research_showcase/users/tests)

### Mock Object Usage Example

Mock objects are crucial for isolating the unit under test from its external dependencies (like external services, email systems, or complex related components). This ensures that the test focuses solely on the logic of the unit itself. We use Python's `unittest.mock.patch` decorator for this purpose.

Here is an example demonstrating the use of mock objects to test the `approve_research` view function in isolation. This test verifies the core logic of approving a project (changing status, saving, redirecting) without actually sending emails or creating real in-app notifications.

**Test Case:** `test_approve_research_isolation` in `research_showcase/research/tests/test_views.py`

```python
# research_showcase/research/tests/test_views.py

# ... other imports ...
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.test import RequestFactory
from research.models import ResearchProject, Notification
from users.models import User
from ..views import approve_research # Function being tested

# ... other test classes ...

class ApproveResearchMockTest(TestCase):
    """Tests for the approve_research view with mock objects."""

    def setUp(self):
        # Create necessary users and a project
        self.faculty_user = User.objects.create_user(
            username="testfaculty", password="password123", role="faculty", email="faculty@test.com"
        )
        self.admin_user = User.objects.create_user(
            username="testadmin_approver", password="password123", role="admin", email="admin@test.com"
        )
        self.project = ResearchProject.objects.create(
            title="Pending Project for Mock Test",
            student_author_name="Test Student",
            abstract="This is a test abstract.",
            approval_status="pending",
            author=self.faculty_user,
            # Add other required fields as necessary
        )
        # Use RequestFactory to create a request object independent of the test client
        self.factory = RequestFactory()

    @patch("research.views.send_status_change_email") # Mock the email sending function
    @patch("research.views.create_in_app_notification") # Mock the notification creation function
    def test_approve_research_isolation(self, mock_notification, mock_email):
        """
        Test the approve_research view in isolation using mocks.
        Verifies:
        1. Project status changes to 'approved'.
        2. Correct redirection occurs.
        3. It sends an email notification (mocked)
        4. It creates an in-app notification (mocked)
        """
        # Create a request object as if coming from the admin user
        # Note: We use RequestFactory here for more direct view testing,
        # but Client.get/post could also be used with mocks.
        request = self.factory.get(reverse("approve_research", args=[self.project.id]))
        request.user = self.admin_user
        request._messages = MagicMock() # Mock the messages framework storage

        # Call the view function directly with the request and project ID
        response = approve_research(request, self.project.id)

        # 1. Check database state
        self.project.refresh_from_db()
        self.assertEqual(self.project.approval_status, "approved")

        # 2. Check response (should be a redirect)
        self.assertEqual(response.status_code, 302) # Status code for redirect
        self.assertEqual(response.url, reverse("review_research"))

        # 3 & 4. Verify mocked functions were called appropriately
        mock_email.assert_called_once()
        mock_notification.assert_called_once()

        # Optional: Inspect arguments passed to mocks
        email_call_args = mock_email.call_args
        self.assertEqual(email_call_args[0][0], self.project) # First arg was the project instance
        self.assertEqual(email_call_args[1]['subject_prefix'], "Research Project Approved")

        notification_call = mock_notification.call_args
        self.assertEqual(notification_call[0][0], self.faculty_user) # First arg was the recipient user
        self.assertTrue("approved and published" in notification_call[0][1]) # Check message content

```

**Explanation:**

1. `@patch("research.views.send_status_change_email")` and `@patch("research.views.create_in_app_notification")`: These decorators replace the actual `send_status_change_email` and `create_in_app_notification` functions within the `research.views` module with mock objects (`mock_email` and `mock_notification`) for the duration of the `test_approve_research_isolation` execution.
2. `mock_email.assert_called_once()` and `mock_notification.assert_called_once()`: These assertions verify that the view logic attempted to call the (now mocked) email and notification functions exactly once, as expected during the approval process.
3. Inspecting Call Arguments: We further check `mock_email.call_args` and `mock_notification.call_args` to ensure these mocked functions were called with the correct arguments (e.g., the correct project instance, user, and subject line/message content).

This approach allows us to test the core logic of the `approve_research` view (database update, redirection) without relying on the actual implementation or potential failures of the external email and notification systems.

**Links:**

- **Class/Function Being Tested:** [`research_showcase/research/views.py#L222`](https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/research/views.py#L222) (approve_research function)
- **Test Case:** [`research_showcase/research/tests/test_views.py#L724`](https://github.com/Naalu/ds-senior-capstone-projects-website/blob/main/research_showcase/research/tests/test_views.py#L722) (test_approve_research_isolation method)

### Test Execution and Coverage

The project aims for high test coverage to ensure reliability. Tests are run using the `coverage` package integrated with Django's test runner.

**Execution Command (from `research_showcase` directory):**

```bash
python -m coverage run manage.py test
```

**Coverage Report Command:**

```bash
coverage report
```

**Successful Test Execution & Coverage Report:**

- ![Test Results](images/Tests_results2.png)
  - The "OK" indicates that all tests passed.
- ![Test Coverage](images/Tests_coverage.png)
  - The coverage report shows the percentage of code that is covered by tests.

The current test coverage is **95%**, meeting our project goal and demonstrating a high degree of verification through automated testing. The tests cover models, forms, views, utility functions, and user workflows, ensuring that core functionalities behave as expected and regressions are caught early. The use of mock objects further enhances the quality by allowing focused unit testing.

## Acceptance Test

An acceptance test is a test that verifies the correct implementation of a feature from the user interface perspective. An acceptance test is a black box test (the system is tested without knowledge about its internal implementation). Provide the following information:

    Test framework you used to develop your tests (e.g., Selenium, Katalon Studio, Espresso2, Cucumber, etc.)
    Link to your GitHub folder where your automated acceptance tests are located.
    An example of an acceptance test. Include in your answer a GitHub link to the test and an explanation about the tested feature.
    A print screen/video showing the acceptance test execution. 

Grading criteria (7 points): adequate choice of a test framework, coverage of the tests, quality of the tests, adequate example of an acceptance test, print screen/video showing successful tests execution.

# Validation

At the beginning of the semester, you talked to the clients/potential users to understand their needs. Now it is time to check if you are on the right track by conducting some user evaluation on the actual system. Include in this deliverable the following information:

Script: The script should have the tasks that you gave to the user, what data you collected, and the questions you asked.
In particular, do not forget to add questions about the users’ general impressions. You can ask open questions (e.g., How would you describe the homepage of our app? How do you compare our system to the competitor X?) or closed questions (On a scale of 1 to 10, how would you rate the layout of our application?
On the same scale, how likely would you use the system in its current state?).
Take a look at the inception and requirements deliverables to help create the script.
Design a script to check if you are achieving your initial goals and if the features are implemented in a satisfactory way.

Results: Conduct the user evaluation with at least 3 users. Report the data that you collected.

## Robert Buscaglia

## Questions and Answer

On a scale of 1 to 10, how would you rate the layout of our application?

    "It's a 9"

From our earlier interview one of your biggest requirements was to allow muliple file formats for project. Were we able to sastisfy that requirement?

    "Yes, each project can have a image file for posters, videos not hosted but linked to is perfect, and then links to various sites pertaining to projects. I don't see any problems here."

You suggested a faculty driven submission process which we ended up pursuing. Do you still support thos method?

    "I still think it is the better way to go about this, and I'm glad you made the switch"

Is there any features we didn't mention previously that you are glad to have in place?

    "The notification system is a great feature. Realistically we would have a dedicated department email for it."

Would you use the project in it's current state?

    "I could use it in it's current state as we still do not have a dedicated place for these projects but I would prefer to have the critiques corrected first. It just needs some refinements to be completly accurate."

## Summary and First Impressions

Dr. Robert Buscaglia first impressions were overall approval of the projects state. From the upload, approval, to searching and browsing the framework he only had minor critques and corrections that we could implement that we had described to him earlier. For example project had a student author, author (as in faculty submission) and collorators. Instead, he mentioned in order to be more accurate is should be student author, faculty advisor, and collaborators and having the faculty who submitted the project more in the backround instead of being listed in the open. He needs that information but whats inportant is the student authors and the faculty advisor the saw over the project whether it be a class project or research. He apprciated the search layout and how each project had thumbnails shown at all times. One of his final statments is that the website is "really useful" he helped us outline a real path to getting the project up the chain in the Mathmatic and Statistics department so that it could be thouroughly reviewed for real implementation.

# 2nd user

## Questions and Answer

## Summary and First Impressions

# 3nd user

## Questions and Answer

## Summary and First Impressions

# Reflection and Refinements

Reflections: Reflect on what you observed. Some questions that you can explore: What features worked well? What can be changed? How is the learning curve of your system? Did the users perform the tasks as you expected? Did the users’ actions produce the results they expected? What did the users like the most? Is your value proposition accomplished?

Grading criteria (17 points): adequate script, adequate report of the results, adequate reflection, language.
