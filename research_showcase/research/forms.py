import os
from typing import List, Optional

from django import forms
from django.core.files.uploadedfile import UploadedFile

from .models import ResearchProject

from datetime import date

# Constants for validation with type annotations
MIN_TITLE_LENGTH: int = 10
MIN_ABSTRACT_LENGTH: int = 100
MAX_POSTER_SIZE_MB: int = 5
MAX_PDF_SIZE_MB: int = 10
MAX_PRESENTATION_SIZE_MB: int = 10
MB_TO_BYTES: int = 1024 * 1024
VALID_POSTER_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf"]
VALID_PRESENTATION_EXTENSIONS: List[str] = ["pdf", "ppt", "pptx"]
VALID_PDF_EXTENSION: str = "pdf"


class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = [
            "title",
            "student_author_name",
            "abstract",
            "collaborator_names",
            "date_presented",
            "github_link",
            "project_sponsor",
            "poster_image",
            "video_link",
            "presentation_file",
            "pdf_file",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter research project title",
                    "data-bs-toggle": "tooltip",
                    "title": "A descriptive title for the research project",
                }
            ),
            "student_author_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter student author name",
                    "data-bs-toggle": "tooltip",
                    "title": "The student who conducted this research",
                }
            ),
            "abstract": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Provide a brief summary of the research",
                    "data-bs-toggle": "tooltip",
                    "title": "A concise summary of the research project (250-500 words recommended)",
                }
            ),
            "collaborator_names": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Enter collaborator names, separated by commas",
                    "data-bs-toggle": "tooltip",
                    "title": "Names of people who collaborated on this project (comma-separated)",
                }
            ),
            "date_presented": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "data-bs-toggle": "tooltip",
                    "title": "Date when this research was presented (if applicable)",
                }
            ),
            "github_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "GitHub Repository URL (optional)",
                    "data-bs-toggle": "tooltip",
                    "title": "Link to the GitHub repository containing project code or materials",
                }
            ),
            "project_sponsor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Project sponsor or funding organization (optional)",
                    "data-bs-toggle": "tooltip",
                    "title": "Name of any organization that sponsored or funded this research",
                }
            ),
            "poster_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png,image/gif,application/pdf",
                    "data-bs-toggle": "tooltip",
                    "title": "Upload a research poster image (JPG, PNG, GIF or PDF format)",
                }
            ),
            "video_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Video Presentation URL (optional)",
                    "data-bs-toggle": "tooltip",
                    "title": "Link to a video presentation of the research (YouTube, Vimeo, etc.)",
                }
            ),
            "presentation_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.ppt,.pptx",
                    "data-bs-toggle": "tooltip",
                    "title": "Upload presentation slides (PDF or PPT format)",
                }
            ),
            "pdf_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf",
                    "data-bs-toggle": "tooltip",
                    "title": "Upload the research paper PDF",
                }
            ),
        }

    def clean_title(self) -> str:
        title: str = self.cleaned_data.get("title", "")
        if len(title) < MIN_TITLE_LENGTH:
            raise forms.ValidationError(
                f"Title must be at least {MIN_TITLE_LENGTH} characters long"
            )
        return title

    def clean_abstract(self) -> str:
        abstract: str = self.cleaned_data.get("abstract", "")
        if len(abstract) < MIN_ABSTRACT_LENGTH:
            raise forms.ValidationError(
                f"Abstract must be at least {MIN_ABSTRACT_LENGTH} characters long"
            )
        return abstract

    def clean_poster_image(self) -> Optional[UploadedFile]:
        poster: Optional[UploadedFile] = self.cleaned_data.get("poster_image")
        if poster and poster.name and poster.size:
            # Check file size
            if poster.size > MAX_POSTER_SIZE_MB * MB_TO_BYTES:
                raise forms.ValidationError(
                    f"Image file too large (max {MAX_POSTER_SIZE_MB}MB)"
                )

            # Validate file extension
            ext: str = os.path.splitext(poster.name)[1][1:].lower()
            if ext not in VALID_POSTER_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file extension. Use {', '.join(VALID_POSTER_EXTENSIONS)}"
                )
        return poster

    def clean_pdf_file(self) -> Optional[UploadedFile]:
        pdf: Optional[UploadedFile] = self.cleaned_data.get("pdf_file")
        if pdf and pdf.name and pdf.size:
            # Check file size
            if pdf.size > MAX_PDF_SIZE_MB * MB_TO_BYTES:
                raise forms.ValidationError(
                    f"PDF file too large (max {MAX_PDF_SIZE_MB}MB)"
                )

            # Validate file extension
            ext: str = os.path.splitext(pdf.name)[1][1:].lower()
            if ext != VALID_PDF_EXTENSION:
                raise forms.ValidationError("File must be a PDF document")
        return pdf

    def clean_presentation_file(self) -> Optional[UploadedFile]:
        pres: Optional[UploadedFile] = self.cleaned_data.get("presentation_file")
        if pres and pres.name and pres.size:
            # Check file size
            if pres.size > MAX_PRESENTATION_SIZE_MB * MB_TO_BYTES:
                raise forms.ValidationError(
                    f"Presentation file too large (max {MAX_PRESENTATION_SIZE_MB}MB)"
                )

            # Validate file extension
            ext: str = os.path.splitext(pres.name)[1][1:].lower()
            if ext not in VALID_PRESENTATION_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file extension. Use {', '.join(VALID_PRESENTATION_EXTENSIONS)}"
                )
        return pres

    # Validate the GitHub link          
    def clean_github_link(self) -> Optional[str]:
        github_link: Optional[str] = self.cleaned_data.get("github_link")
        
        # If the field is empty and not required, return None
        if not github_link:
            return github_link
            
        # Check if it's a valid GitHub URL
        if not (github_link.startswith("https://github.com/") or 
                github_link.startswith("http://github.com/")):
            raise forms.ValidationError("Please enter a valid GitHub repository URL (https://github.com/...)")
        
        # Check if it follows the expected GitHub repo format (github.com/username/repo)
        parts = github_link.split("/")
        if len(parts) < 5:  # https:// + empty + github.com + username + repo
            raise forms.ValidationError("GitHub URL should be in format: https://github.com/username/repository")
        
        return github_link       
    
    # Video link validation
    def clean_video_link(self) -> Optional[str]:
        video_link: Optional[str] = self.cleaned_data.get("video_link")
        
        # If the field is empty and not required, return None
        if not video_link:
            return video_link
        
        # List of common video platforms
        valid_platforms = [
            "youtube.com/watch",
            "youtu.be/",
            "vimeo.com/",
        ]
        
        # Check if the URL contains any of the valid video platforms
        is_valid_platform = any(platform in video_link.lower() for platform in valid_platforms)
        
        if not is_valid_platform:
            raise forms.ValidationError(
                "Please enter a valid video URL:\n"
                "YouTube(youtube.com/watch, youtu.be/) or Vimeo (vimeo.com/)"
            )
        
        # Check if it's a well-formed URL
        if not (video_link.startswith("http://") or video_link.startswith("https://")):
            raise forms.ValidationError("Video link must start with http:// or https://")
        
        return video_link
    
    # Validate the date presented field
    # Ensure that the date is not in the future
    def clean_date_presented(self) -> Optional[date]:
        date_presented: Optional[date] = self.cleaned_data.get("date_presented")
        
        # If the field is empty and not required, return None
        if not date_presented:
            return date_presented
        
        # Check if the date is in the future
        today = date.today()
        if date_presented > today:
            print(f"DEBUG: Invalid date detected: {date_presented} > {today}")  # Debug print
            raise forms.ValidationError(
                f"Date presented ({date_presented}) cannot be in the future (today is {today})"
            )
        
        return date_presented