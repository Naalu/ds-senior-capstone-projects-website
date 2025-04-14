from django.contrib import admin

from .models import Colloquium, ResearchProject, StatusHistory


# Inline admin for Status History
class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    fields = (
        "timestamp",
        "actor",
        "status_from",
        "status_to",
        "comment",
    )  # Fields to display
    readonly_fields = (
        "timestamp",
        "actor",
        "status_from",
        "status_to",
        "comment",
    )  # Make them read-only in the inline view
    extra = 0  # Don't show extra empty forms
    can_delete = False  # Don't allow deleting history from project view
    ordering = ["-timestamp"]


# Admin view for ResearchProject
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "student_author_name",
        "author",  # Submitting faculty
        "submission_date",
        "approval_status",
    )
    list_filter = ("approval_status", "submission_date")
    search_fields = (
        "title",
        "abstract",
        "student_author_name",
        "author__username",  # Search by submitting faculty username
    )
    readonly_fields = ("submission_date",)  # Submission date shouldn't be editable
    # Add the new fields and the inline history
    fieldsets = (
        (None, {"fields": ("title", "student_author_name", "abstract", "author")}),
        (
            "Details",
            {
                "fields": (
                    "collaborator_names",
                    "faculty_advisor",
                    "date_presented",
                    "project_sponsor",
                )
            },
        ),
        (
            "Files & Links",
            {
                "fields": (
                    "poster_image",
                    "presentation_file",
                    "pdf_file",
                    "github_link",
                    "video_link",
                )
            },
        ),
        (
            "Approval Workflow",
            {"fields": ("approval_status", "admin_feedback", "submission_date")},
        ),
    )
    inlines = [StatusHistoryInline]


# Admin view for StatusHistory (optional, for direct viewing/searching if needed)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "timestamp",
        "actor",
        "status_from",
        "status_to",
        "comment",
    )
    list_filter = ("status_to", "timestamp")
    search_fields = ("project__title", "actor__username", "comment")
    readonly_fields = (
        "project",
        "timestamp",
        "actor",
        "status_from",
        "status_to",
        "comment",
    )  # Make all fields read-only


# Register models
admin.site.register(ResearchProject, ResearchProjectAdmin)
admin.site.register(Colloquium)
admin.site.register(StatusHistory, StatusHistoryAdmin)
