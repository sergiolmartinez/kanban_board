# projects/tests/test_serializers.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project, ProjectMembership
from projects.serializers import ProjectSerializer

User = get_user_model()


class ProjectSerializerTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner', password='testpass')
        self.user1 = User.objects.create_user(
            username='user1', password='testpass')
        self.user2 = User.objects.create_user(
            username='user2', password='testpass')
        self.project_data = {
            'name': 'New Project',
            'is_public': True,
            'users': [  # Changed from 'projectmembership_set' to 'users'
                {'user_id': self.user1.id, 'role': 'Member'},
                {'user_id': self.user2.id, 'role': 'Viewer'}
            ]
        }

    def test_create_project_with_memberships(self):
        serializer = ProjectSerializer(data=self.project_data)
        self.assertTrue(serializer.is_valid())
        project = serializer.save(owner=self.owner)

        self.assertEqual(project.name, 'New Project')
        self.assertTrue(project.is_public)
        self.assertEqual(project.owner, self.owner)

        # Directly validate the creation of ProjectMembership instances
        memberships = ProjectMembership.objects.filter(project=project)
        self.assertEqual(memberships.count(), 2)
        self.assertTrue(memberships.filter(user=self.user1).exists())
        self.assertTrue(memberships.filter(user=self.user2).exists())

    def test_update_project_memberships(self):
        project = Project.objects.create(
            name='Initial Project', owner=self.owner)
        # This creates an additional membership in addition to any default "Unassigned" project memberships
        ProjectMembership.objects.create(
            project=project, user=self.user1, role='Viewer')

        updated_data = self.project_data.copy()
        updated_data['name'] = 'Updated Project'

        serializer = ProjectSerializer(project, data=updated_data)
        self.assertTrue(serializer.is_valid())
        updated_project = serializer.save()

        self.assertEqual(updated_project.name, 'Updated Project')
        # Now expecting 2 explicitly managed memberships, not considering the default "Unassigned" project
        self.assertEqual(updated_project.projectmembership_set.count(), 2)

    def test_project_serialization_includes_memberships(self):
        project = Project.objects.create(
            name='New Project', owner=self.owner, is_public=True)
        ProjectMembership.objects.create(
            project=project, user=self.user1, role='Member')
        serializer = ProjectSerializer(project)

        # The default "Unassigned" project's memberships aren't relevant to this serialization test
        self.assertIn('users', serializer.data)
        # One explicitly added member is serialized
        self.assertEqual(len(serializer.data['users']), 1)
