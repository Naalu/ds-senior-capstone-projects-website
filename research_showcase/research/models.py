from typing import List, Tuple

from django.db import models
from django.utils import timezone
from users.models import User

# In research/models.py


class ResearchProject(models.Model):
    """
    Model representing a research project submission.

    A research project is submitted by a faculty member on behalf of a student.
    It includes details about the research, optional files and links, and tracks
    its approval status through the workflow process.

    Fields:
        title: The research project title
        abstract: A detailed description of the research
        author: The faculty member who submitted the project
        student_author_name: Name of the student researcher
        collaborator_names: Text field listing all collaborators
        faculty_advisor: Optional link to faculty advisor user
        submission_date: When the project was submitted
        date_presented: When the research was presented (if applicable)
        approval_status: Current status in the approval workflow
        Various optional fields for links and file attachments
    """

    STATUS_CHOICES: List[Tuple[str, str]] = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("needs_revision", "Needs Revision"),
    ]

    title: models.CharField = models.CharField(max_length=255)
    abstract: models.TextField = models.TextField()

    # Faculty member who submits the research
    author: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="research_projects"
    )

    # New field: Student author (text field, not a user)
    student_author_name: models.CharField = models.CharField(max_length=255, blank=True)

    # New field: Text-based collaborators list, not User objects
    collaborator_names: models.TextField = models.TextField(
        blank=True, help_text="Enter collaborator names, separated by commas"
    )

    faculty_advisor: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="advised_projects",
    )

    submission_date: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    # New field: When the research was presented
    date_presented: models.DateField = models.DateField(null=True, blank=True)

    approval_status: models.CharField = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="pending"
    )

    # Add field for admin feedback
    admin_feedback: models.TextField = models.TextField(blank=True, null=True)

    # Optional Fields (keep existing fields)
    github_link: models.URLField = models.URLField(null=True, blank=True)
    project_sponsor: models.CharField = models.CharField(
        max_length=255, null=True, blank=True
    )
    poster_image: models.FileField = models.FileField(
        upload_to="posters/",
        blank=True,
        null=True,
        verbose_name="Research Poster",
        help_text="Poster image or PDF (max 5MB, allowed: jpg, png, pdf)",
    )
    video_link: models.URLField = models.URLField(null=True, blank=True)
    presentation_file: models.FileField = models.FileField(
        upload_to="presentations/",
        blank=True,
        null=True,
        verbose_name="Presentation Slides",
        help_text="Presentation slides (PDF, PPT, PPTX, max 10MB)",
    )
    pdf_file: models.FileField = models.FileField(
        upload_to="research_papers/",
        blank=True,
        null=True,
        verbose_name="Research Paper (PDF)",
        help_text="PDF of the research paper (max 10MB)",
    )

    # Derived properties for semester/year (optional, for easier querying/display)
    @property
    def year_presented(self):
        return self.date_presented.year if self.date_presented else None

    @property
    def semester_presented(self):
        if not self.date_presented:
            return None
        month = self.date_presented.month
        if 3 <= month <= 5:
            return "Spring"
        if 6 <= month <= 7:
            return "Summer"  # Approx
        if 8 <= month <= 11:
            return "Fall"
        if month == 12 or month <= 2:
            return "Winter"  # Approx
        return None  # Should not happen

    def __str__(self) -> str:
        return self.title


class ProjectImage(models.Model):
    """Represents a single image associated with a ResearchProject."""

    project = models.ForeignKey(
        ResearchProject, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="project_images/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.caption:
            return f"Image for {self.project.title}: {self.caption}"
        else:
            return f"Image for {self.project.title} ({self.image.name})"


class StatusHistory(models.Model):
    """Tracks the status changes and feedback for a ResearchProject."""

    project = models.ForeignKey(
        ResearchProject, on_delete=models.CASCADE, related_name="status_history"
    )
    # User who performed the action (can be null if system generated?)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    status_from = models.CharField(
        max_length=15, choices=ResearchProject.STATUS_CHOICES, null=True, blank=True
    )
    status_to = models.CharField(max_length=15, choices=ResearchProject.STATUS_CHOICES)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Status Histories"

    def __str__(self):
        actor_name = self.actor.username if self.actor else "System"
        return f"{self.project.title} changed to {self.get_status_to_display()} by {actor_name} at {self.timestamp}"


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
