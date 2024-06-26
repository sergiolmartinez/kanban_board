# Generated by Django 4.2.11 on 2024-04-09 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="project", name="created_at",),
        migrations.RemoveField(model_name="project", name="updated_at",),
        migrations.AddField(
            model_name="project",
            name="is_public",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="project",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_projects",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="ProjectMembership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Viewer", "Viewer"),
                            ("Member", "Member"),
                            ("Project Manager", "Project Manager"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"unique_together": {("project", "user")},},
        ),
        migrations.AddField(
            model_name="project",
            name="users",
            field=models.ManyToManyField(
                related_name="assigned_projects",
                through="projects.ProjectMembership",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
