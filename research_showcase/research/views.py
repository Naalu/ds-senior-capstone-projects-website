from datetime import date

from django.conf import settings  # To get default from email
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required
from django.core.exceptions import PermissionDenied  # Import PermissionDenied

# Import Django's email functions and template loader
from django.core.mail import send_mail

# Import Q for complex lookups, and Min/Max for aggregates
from django.db.models import Max, Min, Q
from django.http import Http404  # Import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse  # Import reverse
from users.decorators import admin_required, faculty_required
from users.models import create_in_app_notification  # Import the new function

from .forms import ResearchProjectForm
from .models import ProjectImage, ResearchProject, StatusHistory
from .semester_utils import generate_semesters

# Define the canonical home view here
# def home_view(request):
#     \"\"\"Display the home page.\"\"\"
#     # Fetch some data for the homepage if needed, e.g., recent projects
#     recent_projects = ResearchProject.objects.filter(
#         approval_status="approved"
#     ).order_by("-submission_date")[:5]  # Get latest 5 approved projects
#     context = {"recent_projects": recent_projects}
#     return render(request, "home.html", context)


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
                research_project.author = request.user
                research_project.approval_status = "pending"
                research_project.admin_feedback = None
                research_project.save()

                # Handle multiple image uploads
                images = request.FILES.getlist("project_images")
                for img_file in images:
                    ProjectImage.objects.create(
                        project=research_project, image=img_file
                    )

                # Create initial status history record
                _create_status_history(
                    research_project,
                    request.user,
                    None,  # Initial state has no 'from'
                    "pending",
                    "Project submitted.",
                )

                messages.success(
                    request,
                    "Research project has been successfully submitted and is pending approval!",
                )
                return redirect("submission_success")
            except Exception as e:
                # Add more specific error logging
                print(
                    f"!!! EXCEPTION during project save/image handling: {type(e).__name__}: {e}"
                )  # DEBUG
                import traceback  # DEBUG

                traceback.print_exc()  # DEBUG
                messages.error(request, f"Error saving research project: {str(e)}")
                # Fall through to re-render the form with errors
        else:
            messages.warning(request, "Please correct the errors in the form.")
            # Add print here too
            print(f"--- Form invalid, errors: {form.errors.as_json()} ---")  # DEBUG
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
    # Fetch pending and needs_revision projects
    projects = ResearchProject.objects.filter(
        Q(approval_status="pending") | Q(approval_status="needs_revision")
    ).order_by("-submission_date")

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


# --- Email Sending Utility ---


def send_status_change_email(project, template_name, subject_prefix, feedback=None):
    """Sends an email notification to the faculty author about status change."""
    faculty_user = project.author

    # Check if the user wants email notifications and has an email address
    if (
        not faculty_user
        or not faculty_user.email
        or not faculty_user.notify_by_email_on_status_change
    ):
        if faculty_user and not faculty_user.notify_by_email_on_status_change:
            print(
                f"Skipping email for '{project.title}': User {faculty_user.username} opted out."
            )  # Log skip
        elif not faculty_user or not faculty_user.email:
            # Keep the original warning message behavior for missing user/email
            # We need a request object to use messages.warning, so maybe just print for now
            print(
                f"WARNING: Could not send notification for '{project.title}': Author or email missing."
            )
        # messages.warning(
        #     request, # request is not available in this scope
        #     f"Could not send notification for '{project.title}': Author email missing.",
        # )
        return

    context = {
        "project": project,
        "faculty_name": faculty_user.get_full_name() or faculty_user.username,
        "feedback": feedback or project.admin_feedback or "N/A",
    }

    try:
        # Render subject and message from templates
        email_content = render_to_string(template_name, context)
        # Simple subject extraction (assumes first line is Subject: ...)
        subject = email_content.splitlines()[0]
        message = "\n".join(email_content.splitlines()[1:]).strip()

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use default sender from settings
            recipient_list=[faculty_user.email],
            fail_silently=False,  # Raise error if sending fails
        )
        print(
            f"Status change email sent to {faculty_user.email} for project {project.id}"
        )  # Logging
    except Exception as e:
        # Log the error - replace print with proper logging in production
        print(
            f"ERROR sending status change email for project {project.id} to {faculty_user.email}: {e}"
        )
        # Optionally inform the admin via messages
        # messages.error(request, f"Failed to send email notification to {faculty_user.email}. Error: {e}")


# --- End Email Sending Utility ---


# Helper function to create status history
def _create_status_history(project, actor, status_from, status_to, comment):
    StatusHistory.objects.create(
        project=project,
        actor=actor,
        status_from=status_from,
        status_to=status_to,
        comment=comment,
    )


@admin_required  # Only admins can approve research
def approve_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    old_status = project.approval_status

    # Update approval status and clear feedback
    project.approval_status = "approved"
    project.admin_feedback = None  # Clear feedback on approval
    project.save()

    # Create history record
    _create_status_history(
        project, request.user, old_status, "approved", "Project approved."
    )

    # Send email notification
    send_status_change_email(
        project,
        template_name="research/emails/submission_approved.txt",
        subject_prefix="Research Project Approved",
    )

    # Create in-app notification
    try:
        approval_message = (
            f"Your research project '{project.title}' has been approved and published."
        )
        # Link directly to the public project detail page upon approval
        project_url = reverse("project_detail", args=[project.id])
        create_in_app_notification(project.author, approval_message, project_url)
    except Exception as e:  # Catch potential errors during notification creation
        print(f"Error creating approval notification for project {project.id}: {e}")
        messages.warning(
            request, "Failed to create in-app notification for the author."
        )

    messages.success(
        request,
        f"Research project '{project.title}' by {project.student_author_name} has been approved and published.",
    )
    return redirect("review_research")


@admin_required  # Only admins can reject research
def reject_research(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    old_status = project.approval_status

    if request.method == "POST":
        rejection_reason = request.POST.get(
            "rejection_reason", "No reason provided."
        )  # Provide default

        # Update status and feedback
        project.approval_status = "rejected"
        project.admin_feedback = rejection_reason  # Store the reason
        project.save()

        # Create history record
        _create_status_history(
            project,
            request.user,
            old_status,
            "rejected",
            f"Project rejected. Reason: {rejection_reason}",
        )

        # Send email notification
        send_status_change_email(
            project,
            template_name="research/emails/submission_rejected.txt",
            subject_prefix="Research Project Rejected",
            feedback=rejection_reason,  # Pass feedback explicitly
        )

        # Create in-app notification
        try:
            rejection_message = f"Your research project '{project.title}' was rejected. Reason: {rejection_reason}"
            # Link to the user's submissions list upon rejection
            submissions_url = reverse("my_submissions")
            create_in_app_notification(
                project.author, rejection_message, submissions_url
            )
        except Exception as e:  # Catch potential errors during notification creation
            print(
                f"Error creating rejection notification for project {project.id}: {e}"
            )
            messages.warning(
                request, "Failed to create in-app notification for the author."
            )

        messages.warning(
            request,
            f"Research project '{project.title}' "
            f"by {project.student_author_name} has been rejected. "
            f"Reason Given: {rejection_reason}",
        )
        return redirect("review_research")
    else:
        # Show rejection form (template needs a textarea for rejection_reason)
        return render(
            request,
            "research/reject_research.html",  # Ensure this template has the form
            {"project": project, "page_title": "Reject Research Submission"},
        )


# New view for requesting revisions
@admin_required
def request_revision(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    old_status = project.approval_status

    if request.method == "POST":
        revision_feedback = request.POST.get(
            "revision_feedback", "Revisions requested."
        )  # Provide default

        # Update status and feedback
        project.approval_status = "needs_revision"
        project.admin_feedback = revision_feedback  # Store the feedback
        project.save()

        # Create history record
        _create_status_history(
            project,
            request.user,
            old_status,
            "needs_revision",
            f"Revisions requested. Feedback: {revision_feedback}",
        )

        # Send email notification
        send_status_change_email(
            project,
            template_name="research/emails/submission_revision_requested.txt",
            subject_prefix="Revisions Requested for Research Project",
            feedback=revision_feedback,  # Pass feedback explicitly
        )

        # Create in-app notification
        try:
            revision_message = f"Revisions requested for your project '{project.title}'. Feedback: {revision_feedback}"
            # Link to the edit page upon revision request
            edit_url = reverse("edit_submission", args=[project.id])
            create_in_app_notification(project.author, revision_message, edit_url)
        except Exception as e:  # Catch potential errors during notification creation
            print(
                f"Error creating revision request notification for project {project.id}: {e}"
            )
            messages.warning(
                request, "Failed to create in-app notification for the author."
            )

        messages.info(
            request,
            f"Revisions requested for project '{project.title}'. Feedback provided.",
        )
        return redirect("review_research")
    else:
        # Show revision request form (template needs a textarea for revision_feedback)
        return render(
            request,
            "research/request_revision.html",  # Create this template
            {"project": project, "page_title": "Request Revisions"},
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
    sort_by = request.GET.get("sort_by", "date")  # Default to sorting by date

    # First, determine the date range of all projects in the database
    date_range = ResearchProject.objects.filter(approval_status="approved").aggregate(
        earliest=Min("date_presented"), latest=Max("date_presented")
    )

    earliest_date = date_range["earliest"]
    latest_date = date_range["latest"]

    # If no projects exist, use reasonable defaults
    if not earliest_date or not latest_date:
        current_year = date.today().year
        earliest_date = date(current_year - 2, 1, 1)
        latest_date = date(current_year, 12, 31)

    # Generate semesters covering our data range, plus a buffer
    start_year = earliest_date.year - 1  # Add one year buffer before
    end_year = latest_date.year + 1  # Add one year buffer after

    # Generate all semesters in this range
    semesters = generate_semesters(start_year, end_year)

    # Sort semesters chronologically
    season_order = {"Spring": 0, "Summer": 1, "Fall": 2, "Winter": 3}
    sorted_semesters = sorted(
        semesters.keys(), key=lambda x: (int(x.split()[1]), season_order[x.split()[0]])
    )

    # Determine default selections if none provided
    if not start_semester and sorted_semesters:
        # Find the first semester that contains or precedes the earliest project
        for sem in sorted_semesters:
            if semesters[sem]["end"] >= earliest_date:
                start_semester = sem
                break
        if not start_semester:  # Fallback
            start_semester = sorted_semesters[0]

    if not end_semester and sorted_semesters:
        # Find the last semester that contains or follows the latest project
        for sem in reversed(sorted_semesters):
            if semesters[sem]["start"] <= latest_date:
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
        start_date = semesters[start_semester]["start"]

    if end_semester and end_semester in semesters:
        end_date = semesters[end_semester]["end"]

    # Build the query with prefetching for efficiency
    projects_query = ResearchProject.objects.filter(
        approval_status="approved"
    ).prefetch_related("images")  # Prefetch related ProjectImage objects

    # Apply text search if provided
    if query:
        projects_query = projects_query.filter(
            Q(title__icontains=query)
            | Q(abstract__icontains=query)
            | Q(project_sponsor__icontains=query)
        )

    # Apply date filtering if provided
    if start_date:
        projects_query = projects_query.filter(date_presented__gte=start_date)

    if end_date:
        projects_query = projects_query.filter(date_presented__lte=end_date)

    # Apply sorting before final processing
    sort_order = "title" if sort_by == "title" else "-date_presented"
    projects_list = list(
        projects_query.order_by(sort_order)
    )  # Execute query and get list

    # Process list to add thumbnail URL
    for project in projects_list:
        project.thumbnail_url = None  # Default to None
        first_image = (
            project.images.first()
        )  # Get first related image (uses prefetched data)
        if first_image:
            project.thumbnail_url = first_image.image.url
        elif project.poster_image:  # Check poster image if no project images exist
            project.thumbnail_url = project.poster_image.url

    # Ensure sort_by is correctly set for the template context
    if sort_by != "title":
        sort_by = "date"

    context = {
        "projects": projects_list,  # Pass the processed list
        "query": query,
        "semesters": sorted_semesters,
        "start_semester": start_semester,
        "end_semester": end_semester,
        "sort_by": sort_by,
    }

    return render(request, "research/search_results.html", context)


# --- Project Detail View ---


def project_detail(request, project_id):
    """Display details of a single research project."""
    project = get_object_or_404(ResearchProject, id=project_id)

    # Ensure only approved projects are publicly visible
    if project.approval_status != "approved":
        raise Http404("Project not found or not approved.")

    # Prefetch related images for efficiency
    project_images = project.images.all()

    context = {
        "project": project,
        "project_images": project_images,
        "page_title": project.title,
    }
    return render(request, "research/project_detail.html", context)


# --- Faculty Workflow Views ---


@faculty_required
def my_submissions(request):
    """Display a list of research projects submitted by the logged-in faculty user."""
    projects = ResearchProject.objects.filter(author=request.user).order_by(
        "-submission_date"
    )
    context = {"projects": projects, "page_title": "My Submissions"}
    return render(request, "research/my_submissions.html", context)


@login_required  # Keep login required for editing
@faculty_required  # Ensure user is faculty
def edit_submission(request, project_id):
    """Allows faculty to edit their submissions, typically after revision request."""
    project = get_object_or_404(ResearchProject, id=project_id)
    old_status = project.approval_status

    # --- Permission Checks ---
    # 1. Check if the logged-in user is the author
    if project.author != request.user:
        raise PermissionDenied("You do not have permission to edit this project.")

    # 2. Check if the project is actually in 'needs_revision' status
    if project.approval_status != "needs_revision":
        messages.error(
            request,
            "This project cannot be edited as it is not currently awaiting revision.",
        )
        return redirect(
            "my_submissions"
        )  # Redirect instead of 403 to be more user-friendly here
    # --- End Permission Checks ---

    if request.method == "POST":
        form = ResearchProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            try:
                updated_project = form.save(commit=False)
                # Reset status to pending and clear feedback upon successful edit
                updated_project.approval_status = "pending"
                updated_project.admin_feedback = None
                updated_project.save()

                # Handle updated images (optional: clear old images first?)
                # For simplicity, this example just adds new images if provided
                images = request.FILES.getlist("project_images")
                if images:
                    # Optional: Clear existing images first if desired
                    # ProjectImage.objects.filter(project=updated_project).delete()
                    for img_file in images:
                        ProjectImage.objects.create(
                            project=updated_project, image=img_file
                        )

                # Create history record for the edit/resubmission
                _create_status_history(
                    updated_project,
                    request.user,
                    old_status,
                    "pending",
                    "Project updated and resubmitted by author.",
                )

                # Correct flash message
                messages.success(
                    request,
                    f"Project '{updated_project.title}' updated and resubmitted for approval.",
                )
                return redirect("my_submissions")
            except Exception as e:
                messages.error(request, f"Error updating research project: {str(e)}")
        else:
            messages.warning(request, "Please correct the errors in the form.")
    else:
        form = ResearchProjectForm(instance=project)

    context = {
        "form": form,
        "project": project,  # Pass project to context for template access
        "page_title": f"Edit Submission: {project.title}",
    }
    return render(request, "research/edit_submission.html", context)


@login_required  # Only logged-in users can view history
def project_history(request, project_id):
    """Displays the status history for a specific research project."""
    project = get_object_or_404(ResearchProject, id=project_id)

    # Permission Check: Only the author or an admin can view history
    if not (project.author == request.user or request.user.is_admin()):
        raise PermissionDenied(
            "You do not have permission to view this project's history."
        )

    history_entries = (
        project.status_history.all()
    )  # Fetches related StatusHistory objects

    context = {
        "project": project,
        "history_entries": history_entries,
        "page_title": f"History for {project.title}",
    }
    return render(request, "research/project_history.html", context)
