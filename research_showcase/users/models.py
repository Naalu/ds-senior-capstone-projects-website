from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("faculty", "Faculty"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def is_student(self):
        return self.role == "student"

    def is_faculty(self):
        return self.role == "faculty"

    def is_admin(self):
        return self.role == "admin"
