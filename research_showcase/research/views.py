from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from users.decorators import faculty_required, student_required

from .forms import ResearchProjectForm
from .models import ResearchProject


@student_required  # Restrict submission to students only
def submit_research(request):
    if request.method == "POST":
        form = ResearchProjectForm(request.POST, request.FILES)
        if form.is_valid():
            research_project = form.save(commit=False)
            research_project.author = request.user  # Assign logged-in user as author
            research_project.save()
            messages.success(request, "Your research project has been submitted!")
            return redirect("submit_research")  # Ensure valid redirect
    else:
        form = ResearchProjectForm()

    return render(request, "research/submit_research.html", {"form": form})


@faculty_required
def review_research(request):
    projects = ResearchProject.objects.filter(approval_status="pending")

    for project in projects:
        # Safely check all optional fields
        project.has_paper = bool(project.pdf_file)  # PDF exists
        project.has_poster = bool(project.poster_image)  # Poster exists
        project.has_presentation = bool(project.presentation_file)  # Slides exist
        project.has_github = bool(project.github_link)  # GitHub link exists
        project.has_video = bool(project.video_link)  # Video link exists
        project.has_sponsor = bool(project.project_sponsor)  # Sponsor exists
        project.has_collaborators = (
            project.collaborators.exists()
        )  # Collaborators exist

    return render(
        request, "research/review_research.html", {"projects": projects}
    )  # Key updated


@faculty_required
def approve_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    project.approval_status = "approved"
    project.save()
    messages.success(request, "Project approved!")
    return redirect("review_research")


@faculty_required
def reject_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    project.approval_status = "rejected"
    project.save()
    messages.error(request, "Project rejected.")
    return redirect("review_research")
