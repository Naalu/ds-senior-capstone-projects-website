from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from users.decorators import admin_required, faculty_required

from .forms import ResearchProjectForm
from .models import ResearchProject


@faculty_required  # Faculty can submit research
def submit_research(request):
    """
    View for faculty to submit student research projects.

    This view handles the multi-step form for research submission,
    including validation and saving. Upon successful submission,
    redirects to a success page.

    Args:
        request: The HTTP request object

    Returns:
        Rendered form template or redirect to success page
    """
    if request.method == "POST":
        form = ResearchProjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                research_project = form.save(commit=False)
                research_project.author = request.user  # Set faculty as author
                research_project.save()

                messages.success(
                    request,
                    "Research project has been successfully submitted and is pending approval!",
                )
                return redirect("submission_success")
            except Exception as e:
                messages.error(request, f"Error saving research project: {str(e)}")
        else:
            messages.warning(request, "Please correct the errors in the form.")
    else:
        form = ResearchProjectForm()

    context = {
        "form": form,
        "page_title": "Submit Research Project",
    }
    return render(request, "research/submit_research.html", context)


@faculty_required  # Only faculty can view submission success page
def submission_success(request):
    """Display a success page after successful research submission"""
    return render(request, "research/submission_success.html")


@admin_required  # Only admins can review research
def review_research(request):
    """
    View for administrators to review pending research submissions.

    Displays a table of all pending research projects with their details
    and provides options to approve or reject each submission.

    Args:
        request: The HTTP request object

    Returns:
        Rendered template with list of pending projects
    """
    # Get all pending research projects
    projects = ResearchProject.objects.filter(approval_status="pending").order_by(
        "-submission_date"
    )

    # Process projects for display
    for project in projects:
        # Check file attachments
        project.has_paper = bool(project.pdf_file)
        project.has_poster = bool(project.poster_image)
        project.has_presentation = bool(project.presentation_file)

        # Check links
        project.has_github = bool(project.github_link)
        project.has_video = bool(project.video_link)

        # Format collaborators for display if needed
        if project.collaborator_names:
            # If it's a long list, truncate it for the table view
            if len(project.collaborator_names) > 100:
                project.collaborators_display = project.collaborator_names[:100] + "..."
            else:
                project.collaborators_display = project.collaborator_names
        else:
            project.collaborators_display = "None"

    return render(
        request,
        "research/review_research.html",
        {"projects": projects, "page_title": "Review Research Submissions"},
    )


@admin_required  # Only admins can approve research
def approve_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)

    # Update approval status
    project.approval_status = "approved"
    project.save()

    # Create detailed success message
    messages.success(
        request,
        f"Research project '{project.title}' by {project.student_author_name} has been approved and published.",
    )

    return redirect("review_research")


@admin_required  # Only admins can reject research
def reject_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)

    if request.method == "POST":
        # Get rejection reason from form
        rejection_reason = request.POST.get("rejection_reason", "")

        # Update approval status
        project.approval_status = "rejected"
        project.save()

        # Create detailed rejection message
        messages.warning(
            request,
            f"Research project '{project.title}' "
            f"by {project.student_author_name} has been rejected. "
            f"Reason Given: {rejection_reason}",
        )

        return redirect("review_research")
    else:
        # Show rejection form
        return render(
            request,
            "research/reject_research.html",
            {"project": project, "page_title": "Reject Research Submission"},
        )


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
