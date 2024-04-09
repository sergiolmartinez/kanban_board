# projects/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Project


@receiver(post_save, sender=User)
def create_default_project(sender, instance, created, **kwargs):
    if created:
        Project.objects.create(
            name="Unassigned", owner=instance, is_public=False)
