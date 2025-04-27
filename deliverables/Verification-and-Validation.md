# Description

Northern Arizona University Department of Mathematics & Statistics Research Showcase is dedicated to developing a web-based platform for Northern Arizona University's Department of Mathematics & Statistics. This platform aims to organize, archive, and showcase student research, particularly senior capstone projects, with potential expansions for additional research and other departments.

# Verification

Verification aims to ensure that you correctly developed the product. 

For this deliverable, show an example of a unit test that uses mock objects to isolate the class from the rest of the system. 

    Test framework you used to develop your tests (e.g., JUnit, unittest, pytest, etc.)
    Link to your GitHub folder where your automated unit tests are located.
    An example of a test case that makes use of mock objects. Include in your answer a GitHub link to the class being tested and to the test.
    A print screen showing the result of the unit tests execution. 

Grading criteria (5 points): adequate choice of a test framework, coverage of the tests, quality of the tests, adequate use of Mock objects, and a print screen showing successful test execution.

# Acceptance Test

This project used the automated tests developed using **Django's built-in testing framework**. This framework is based on Python's standard `unittest` module and provides tools specifically tailored for testing Django applications, including:

- `django.test.TestCase`: A subclass of `unittest.TestCase` that handles database setup/teardown for each test and provides Django-specific assertions.
- `django.test.Client`: A test client used to simulate user interactions with the application via HTTP requests (GET, POST) without needing a running development server.

( Include in your answer a GitHub link to the test and an explanation about the tested feature.
    A print screen/video showing the acceptance test execution. )


# Validation

At the beginning of the semester, you talked to the clients/potential users to understand their needs. Now it is time to check if you are on the right track by conducting some user evaluation on the actual system. Include in this deliverable the following information:

Script: The script should have the tasks that you gave to the user, what data you collected, and the questions you asked. 
In particular, do not forget to add questions about the users’ general impressions. You can ask open questions (e.g., How would you describe the homepage of our app? How do you compare our system to the competitor X?) or closed questions (On a scale of 1 to 10, how would you rate the layout of our application?
On the same scale, how likely would you use the system in its current state?).
Take a look at the inception and requirements deliverables to help create the script. 
Design a script to check if you are achieving your initial goals and if the features are implemented in a satisfactory way. 

Results: Conduct the user evaluation with at least 3 users. Report the data that you collected.

## Robert Buscaglia:

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

Through building the Senior Capstone Projects Website, the undergraduate development team gained real-world experience in full-stack web development, working with Django for the backend and HTML/CSS/ for the frontend. We learned to design a relational database, manage models using Django ORM, and adhere to coding practices and operations effectively.

The team improved their skills in version control with Git, collaborative coding through pull requests and issue tracking, and sees the importance of clear project organization and documentation. We also deepened our understanding of user authentication, form handling, and the challenges of deploying a Django site.

Beyond technical skills, we executed team communication, problem-solving, and adapting to changing project requirements — key parts of professional software development.