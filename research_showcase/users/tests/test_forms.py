from django.test import TestCase

from ..forms import NotificationPreferenceForm


class NotificationPreferenceFormTests(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "notify_by_email_on_status_change": True,
            "notify_in_app_on_status_change": False,
        }
        form = NotificationPreferenceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_checkbox_widgets(self):
        form = NotificationPreferenceForm()
        self.assertIn(
            'class="form-check-input"',
            form.fields["notify_by_email_on_status_change"].widget.render(
                "notify_by_email_on_status_change", True
            ),
        )
        self.assertIn(
            'class="form-check-input"',
            form.fields["notify_in_app_on_status_change"].widget.render(
                "notify_in_app_on_status_change", True
            ),
        )
