from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

"""
Role-Based Access Control Decorators
------------------------------------
These decorators restrict access to views based on the user's role in the system.

USAGE:
- Apply the appropriate decorator above a view function to ensure that only users with the required role can access it.
- Users without the required role will be redirected to the login page.
"""


def faculty_required(view_func):
    """
    Decorator to restrict access to faculty members and administrators.

    Both faculty members and administrators can access views decorated with this decorator.
    Users without these roles will be redirected to the login page.
    """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse("login")
            next_url = request.path
            return redirect(f"{login_url}?next={next_url}")
        if request.user.is_faculty() or request.user.is_admin():
            return view_func(request, *args, **kwargs)
        # Authenticated, but wrong role -> Forbidden
        raise PermissionDenied

    return wrapper


def admin_required(view_func):
    """
    Decorator to restrict access to administrators only.

    Users without the admin role will be redirected to the login page if not authenticated,
    or receive a 403 Forbidden error if authenticated but not an admin.
    """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse("login")
            next_url = request.path
            return redirect(f"{login_url}?next={next_url}")
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)
        # Authenticated, but not admin -> Forbidden
        raise PermissionDenied

    return wrapper
