from django import forms

from .models import ResearchProject


class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = [
            "title",
            "abstract",
            "github_link",
            "project_sponsor",
            "poster_image",
            "video_link",
            "presentation_file",
            "pdf_file",
        ]
        widgets = {
            "abstract": forms.Textarea(attrs={"rows": 4}),
            "github_link": forms.URLInput(
                attrs={"placeholder": "GitHub Repository URL"}
            ),
            "video_link": forms.URLInput(
                attrs={"placeholder": "Video Presentation URL"}
            ),
            "poster_image": forms.ClearableFileInput(),
            "presentation_file": forms.ClearableFileInput(),
            "pdf_file": forms.ClearableFileInput(),
        }
