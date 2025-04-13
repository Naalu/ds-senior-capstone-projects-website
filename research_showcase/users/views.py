from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import NotificationPreferenceForm


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

                # Redirect based on user role
                if user.is_superuser:
                    return redirect("/admin/")
                elif user.is_admin():
                    return redirect("review_research")
                elif user.is_faculty():
                    return redirect("submit_research")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


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
