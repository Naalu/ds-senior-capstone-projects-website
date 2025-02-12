from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def home_view(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            # Redirect based on user role
            if user.is_superuser:
                return redirect("/admin/")
            elif hasattr(user, "role"):
                if user.role == "student":
                    return redirect("submit_research")
                elif user.role == "faculty":
                    return redirect("review_research")
            return redirect("home")  # Default fallback

        else:
            # Provide a more detailed message
            if not username or not password:
                messages.error(request, "Both username and password are required.")
            else:
                messages.error(
                    request, "Invalid username or password. Please try again."
                )

    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home")
