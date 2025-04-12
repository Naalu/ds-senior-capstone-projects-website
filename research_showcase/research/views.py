from django.contrib import messages
from django.db.models import Q, Min, Max
from django.shortcuts import get_object_or_404, redirect, render
from users.decorators import admin_required, faculty_required

from .forms import ResearchProjectForm
from .models import ResearchProject

from .semester_utils import SEMESTERS, generate_semesters
from datetime import date

# Define the canonical home view here
def home_view(request):
    """Display the home page."""
    # Fetch some data for the homepage if needed, e.g., recent projects
    recent_projects = ResearchProject.objects.filter(
        approval_status="approved"
    ).order_by("-submission_date")[:5]  # Get latest 5 approved projects
    context = {"recent_projects": recent_projects}
    return render(request, "home.html", context)


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
    start_semester = request.GET.get("start_semester", "")
    end_semester = request.GET.get("end_semester", "")
    
    # First, determine the date range of all projects in the database
    date_range = ResearchProject.objects.filter(
        approval_status="approved"
    ).aggregate(
        earliest=Min('date_presented'),
        latest=Max('date_presented')
    )
    
    earliest_date = date_range['earliest']
    latest_date = date_range['latest']
    
    # If no projects exist, use reasonable defaults
    if not earliest_date or not latest_date:
        current_year = date.today().year
        earliest_date = date(current_year - 2, 1, 1)
        latest_date = date(current_year, 12, 31)
    
    # Generate semesters covering our data range, plus a buffer
    start_year = earliest_date.year - 1  # Add one year buffer before
    end_year = latest_date.year + 1      # Add one year buffer after
    
    # Generate all semesters in this range
    semesters = generate_semesters(start_year, end_year)
    
    # Sort semesters chronologically
    season_order = {'Spring': 0, 'Summer': 1, 'Fall': 2, 'Winter': 3}
    sorted_semesters = sorted(
        semesters.keys(),
        key=lambda x: (int(x.split()[1]), season_order[x.split()[0]])
    )
    
    # Determine default selections if none provided
    if not start_semester and sorted_semesters:
        # Find the first semester that contains or precedes the earliest project
        for sem in sorted_semesters:
            if semesters[sem]['end'] >= earliest_date:
                start_semester = sem
                break
        if not start_semester:  # Fallback
            start_semester = sorted_semesters[0]
    
    if not end_semester and sorted_semesters:
        # Find the last semester that contains or follows the latest project
        for sem in reversed(sorted_semesters):
            if semesters[sem]['start'] <= latest_date:
                end_semester = sem
                break
        if not end_semester:  # Fallback
            end_semester = sorted_semesters[-1]

    if start_semester in semesters and end_semester in semesters:
        start_idx = sorted_semesters.index(start_semester)
        end_idx = sorted_semesters.index(end_semester)
        
        if start_idx > end_idx:
            # Swap them
            start_semester, end_semester = end_semester, start_semester
    
    # Convert selected semesters to dates for filtering
    start_date = None
    end_date = None
    
    if start_semester and start_semester in semesters:
        start_date = semesters[start_semester]['start']
    
    if end_semester and end_semester in semesters:
        end_date = semesters[end_semester]['end']
    
    # Build the query
    projects_query = ResearchProject.objects.filter(approval_status="approved")
    
    # Apply text search if provided
    if query:
        projects_query = projects_query.filter(
            Q(title__icontains=query) |
            Q(abstract__icontains=query) |
            Q(project_sponsor__icontains=query)
        )
    
    # Apply date filtering if provided
    if start_date:
        projects_query = projects_query.filter(date_presented__gte=start_date)
    
    if end_date:
        projects_query = projects_query.filter(date_presented__lte=end_date)
    
    # Order results
    projects = projects_query.order_by("-date_presented")
    
    context = {
        'projects': projects,
        'query': query,
        'semesters': sorted_semesters,
        'start_semester': start_semester,
        'end_semester': end_semester
    }
    
    return render(request, 'research\search_results.html', context)