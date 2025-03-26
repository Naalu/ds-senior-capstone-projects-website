from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from users.decorators import admin_required, faculty_required

from .forms import ResearchProjectForm
from .models import ResearchProject


@faculty_required  # Faculty can submit research
def submit_research(request):
    if request.method == "POST":
        form = ResearchProjectForm(request.POST, request.FILES)
        if form.is_valid():
            research_project = form.save(commit=False)
            research_project.author = request.user  # Assign logged-in user as author
            research_project.save()
            messages.success(request, "Research project has been submitted!")
            return redirect("submit_research")
    else:
        form = ResearchProjectForm()

    return render(request, "research/submit_research.html", {"form": form})


@admin_required  # Only admins can review research
def review_research(request):
    projects = ResearchProject.objects.filter(approval_status="pending")

    for project in projects:
        # Safely check all optional fields
        project.has_paper = bool(project.pdf_file)
        project.has_poster = bool(project.poster_image)
        project.has_presentation = bool(project.presentation_file)
        project.has_github = bool(project.github_link)
        project.has_video = bool(project.video_link)
        project.has_sponsor = bool(project.project_sponsor)
        project.has_collaborators = project.collaborators.exists()

    return render(request, "research/review_research.html", {"projects": projects})


@admin_required  # Only admins can approve research
def approve_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    project.approval_status = "approved"
    project.save()
    messages.success(request, "Project approved!")
    return redirect("review_research")


@admin_required  # Only admins can reject research
def reject_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    project.approval_status = "rejected"
    project.save()
    messages.error(request, "Project rejected.")
    return redirect("review_research")


def search_research(request):
    """
    Search for research projects by title, abstract, or project sponsor.

    This view handles searching of approved research projects. When a query
    is provided, it filters projects containing the search term in their
    title, abstract, or project sponsor fields. Without a query, it returns
    all approved projects.

    Args:
        request: The HTTP request object containing the 'q' query parameter

    Returns:
        Rendered template with filtered research projects and the search query
    """
    query = request.GET.get("q", "")
    projects = None

    if query:
        projects = ResearchProject.objects.filter(
            Q(title__icontains=query)
            | Q(abstract__icontains=query)
            | Q(project_sponsor__icontains=query),
            approval_status="approved",
        ).order_by("-submission_date")
    else:
        projects = ResearchProject.objects.filter(approval_status="approved").order_by(
            "-submission_date"
        )

    return render(
        request, "research/search_results.html", {"projects": projects, "query": query}
    )
