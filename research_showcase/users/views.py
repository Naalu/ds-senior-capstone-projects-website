from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import NotificationPreferenceForm
from .models import Notification


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")

                # Check for 'next' parameter for redirection
                next_url = request.POST.get("next") or request.GET.get("next")
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)

                # Fallback to role-based redirection if 'next' is invalid or not present
                if user.is_superuser:
                    return redirect("/admin/")
                elif user.is_admin():
                    return redirect("review_research")
                elif user.is_faculty():
                    return redirect("submit_research")
                return redirect("home")  # Default fallback
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    # Determine next_url consistently after handling POST/GET
    next_url = request.POST.get("next", request.GET.get("next"))

    return render(
        request,
        "users/login.html",
        {
            "form": form,
            "next": next_url,  # Add next to context for hidden input
        },
    )


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home")


@login_required
def edit_profile(request):
    """View for users to edit their notification preferences."""
    if request.method == "POST":
        form = NotificationPreferenceForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your notification preferences have been updated."
            )
            return redirect("edit_profile")  # Redirect back to the same page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NotificationPreferenceForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


@require_POST
@login_required
def mark_notifications_read(request):
    """Marks all unread notifications for the current user as read."""
    try:
        # Update notifications in bulk for efficiency
        num_updated = Notification.objects.filter(
            recipient=request.user, read=False
        ).update(read=True)
        return JsonResponse({"success": True, "marked_read_count": num_updated})
    except Exception as e:
        # Log the error ideally
        print(
            f"Error marking notifications as read for user {request.user.username}: {e}"
        )
        return JsonResponse({"success": False, "error": str(e)}, status=500)
