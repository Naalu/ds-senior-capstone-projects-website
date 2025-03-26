from django.db import models
from users.models import User


class ResearchProject(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    title: models.CharField = models.CharField(max_length=255)
    abstract: models.TextField = models.TextField()  # Written abstract
    author: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="research_projects"
    )
    collaborators: models.ManyToManyField = models.ManyToManyField(
        User, related_name="collaborations", blank=True
    )
    faculty_advisor: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="advised_projects",
    )
    submission_date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    approval_status: models.CharField = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )

    # Optional Fields
    github_link: models.URLField = models.URLField(
        null=True, blank=True
    )  # GitHub Repository
    project_sponsor: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )  # Sponsor organization or company
    poster_image: models.ImageField = models.ImageField(
        upload_to="posters/", null=True, blank=True
    )  # Research poster image
    video_link: models.URLField = models.URLField(
        null=True, blank=True
    )  # Video Presentation Link
    presentation_file = models.FileField(
        upload_to="presentations/", null=True, blank=True
    )  # Slide Presentation
    pdf_file: models.FileField = models.FileField(
        upload_to="research_papers/", null=True, blank=True
    )  # Research Paper PDF

    def __str__(self):
        return self.title


class Colloquium(models.Model):
    title: models.CharField = models.CharField(max_length=255)
    presenter: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    date: models.DateField = models.DateField()
    description: models.TextField = models.TextField()
    video_link: models.URLField = models.URLField(
        null=True, blank=True
    )  # Existing field for recorded talk
    presentation_file: models.FileField = models.FileField(
        upload_to="colloquium_presentations/", null=True, blank=True
    )  # New field

    def __str__(self):
        return f"{self.title} by {self.presenter.username} on {self.date}"
