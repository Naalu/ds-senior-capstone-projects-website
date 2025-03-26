# Description: Custom management command to create a superuser with admin role

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a superuser with admin role"

    def handle(self, *args, **kwargs):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username, email=email, password=password
            )
            user.role = "admin"
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with admin role'
                )
            )
        else:
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
