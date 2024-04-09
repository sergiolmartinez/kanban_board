from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project


class Command(BaseCommand):
    help = 'Creates a default "Unassigned" project for all existing users who do not have one.'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            # Check if the user already has an "Unassigned" project
            if not Project.objects.filter(owner=user, name="Unassigned").exists():
                # Create the "Unassigned" project for the user
                Project.objects.create(name="Unassigned", owner=user)
                print(f'Created "Unassigned" project for {user.username}')
            else:
                print(f'{user.username} already has an "Unassigned" project')
