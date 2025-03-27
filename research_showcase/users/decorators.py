from django.shortcuts import redirect

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
        if request.user.is_authenticated and (
            request.user.is_faculty() or request.user.is_admin()
        ):
            return view_func(request, *args, **kwargs)
        return redirect("login")

    return wrapper


def admin_required(view_func):
    """
    Decorator to restrict access to administrators only.

    Users without the admin role will be redirected to the login page.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin():
            return view_func(request, *args, **kwargs)
        return redirect("login")

    return wrapper
