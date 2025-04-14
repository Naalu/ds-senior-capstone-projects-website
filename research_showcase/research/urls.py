from django.urls import path

from .views import (
    approve_research,
    edit_submission,
    my_submissions,
    project_detail,
    project_history,
    reject_research,
    request_revision,
    review_research,
    search_research,
    submission_success,
    submit_research,
)

urlpatterns = [
    path("submit/", submit_research, name="submit_research"),
    path("submissions/", my_submissions, name="my_submissions"),
    path("submissions/edit/<int:project_id>/", edit_submission, name="edit_submission"),
    path("review/", review_research, name="review_research"),
    path("approve/<int:project_id>/", approve_research, name="approve_research"),
    path("reject/<int:project_id>/", reject_research, name="reject_research"),
    path("revise/<int:project_id>/", request_revision, name="request_revision"),
    path("search/", search_research, name="search_research"),
    path("submit/success/", submission_success, name="submission_success"),
    path("project/<int:project_id>/", project_detail, name="project_detail"),
    path("project/<int:project_id>/history/", project_history, name="project_history"),
]
