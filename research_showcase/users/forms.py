from django import forms

from .models import User


class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["notify_by_email_on_status_change", "notify_in_app_on_status_change"]
        labels = {
            "notify_by_email_on_status_change": "Receive email notifications for project status changes?",
            "notify_in_app_on_status_change": "Receive in-app notifications for project status changes?",
        }
        help_texts = {
            "notify_by_email_on_status_change": "If checked, you will receive emails when your submitted projects are approved, rejected, or need revisions.",
            "notify_in_app_on_status_change": "If checked, you will see notifications within the website (feature under development).",
        }
        # Add form-check-input class for Bootstrap styling of checkboxes
        widgets = {
            "notify_by_email_on_status_change": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "notify_in_app_on_status_change": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
