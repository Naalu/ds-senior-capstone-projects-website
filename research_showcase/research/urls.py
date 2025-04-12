from django.urls import path

from .views import (
    approve_research,
    home_view,
    reject_research,
    review_research,
    search_research,
    submission_success,
    submit_research,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("submit/", submit_research, name="submit_research"),
    path("review/", review_research, name="review_research"),
    path("approve/<int:project_id>/", approve_research, name="approve_research"),
    path("reject/<int:project_id>/", reject_research, name="reject_research"),
    path("search/", search_research, name="search_research"),
    path("submit/success/", submission_success, name="submission_success"),
]
