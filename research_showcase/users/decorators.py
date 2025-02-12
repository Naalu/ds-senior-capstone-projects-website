from django.shortcuts import redirect

"""
Role-Based Access Control Decorators
------------------------------------
These decorators restrict access to views based on the user's role in the system.

USAGE:
- Apply the appropriate decorator above a view function to ensure that only users with the required role can access it.
- Users without the required role will be redirected to the login page.

EXAMPLES:

1. Restricting a faculty-only dashboard:
    from users.decorators import faculty_required

    @faculty_required
    def faculty_dashboard(request):
        return render(request, 'faculty/dashboard.html')

2. Restricting research submission to students only:
    from users.decorators import student_required

    @student_required
    def submit_research(request):
        return render(request, 'research/submit.html')

3. Restricting an admin-only view:
    from users.decorators import admin_required

    @admin_required
    def admin_dashboard(request):
        return render(request, 'admin/dashboard.html')

CONTRIBUTOR NOTES:
- **Ensure that all restricted views are properly decorated** to prevent unauthorized access.
- **Use the correct decorator** based on the intended audience of the view.
- **Test role-based access** after applying a decorator to confirm that only users with the correct role can access the view.
- **Secure navigation elements in templates** to prevent users from seeing links they do not have access to.

"""


def student_required(view_func):
    """Decorator to restrict access to students only."""

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student():
            return view_func(request, *args, **kwargs)
        return redirect("login")

    return wrapper


def faculty_required(view_func):
    """Decorator to restrict access to faculty members only."""

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_faculty():
            return view_func(request, *args, **kwargs)
        return redirect("login")

    return wrapper


def admin_required(view_func):
    """Decorator to restrict access to administrators only."""

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin():
            return view_func(request, *args, **kwargs)
        return redirect("login")

    return wrapper
