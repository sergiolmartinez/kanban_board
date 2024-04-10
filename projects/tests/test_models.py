# projects/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project, ProjectMembership

User = get_user_model()


class ProjectModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user for the owner of the project
        cls.owner = User.objects.create_user(
            username='owner', password='testpassword')
        # Create another user for testing project membership
        cls.member = User.objects.create_user(
            username='member', password='testpassword')
        # Create a project
        cls.project = Project.objects.create(
            name="Test Project", owner=cls.owner, is_public=True)
        # Create a project membership
        cls.membership = ProjectMembership.objects.create(
            project=cls.project, user=cls.member, role='Member')

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.owner, self.owner)
        self.assertTrue(self.project.is_public)

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_membership(self):
        # Ensure the member is correctly assigned to the project with the right role
        self.assertTrue(ProjectMembership.objects.filter(
            project=self.project, user=self.member, role='Member').exists())
        # Check the reverse relation from user to projects they're assigned to
        self.assertTrue(self.member.assigned_projects.filter(
            id=self.project.id).exists())

    def test_project_ownership(self):
        # Ensure the owner is correctly associated with the project
        self.assertEqual(self.project.owner, self.owner)
        # Check the reverse relation from owner to projects they own
        self.assertTrue(self.owner.owned_projects.filter(
            id=self.project.id).exists())
