# projects/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from projects.models import Project, ProjectMembership


class ProjectViewSetTest(APITestCase):
    def setUp(self):
        # Create users
        self.user_owner = User.objects.create_user(
            username='owner', password='pass')
        self.user_member = User.objects.create_user(
            username='member', password='pass')
        self.user_non_member = User.objects.create_user(
            username='non_member', password='pass')

        # Create project
        self.project = Project.objects.create(
            name='Test Project', owner=self.user_owner, is_public=False)

        # Authenticate as project owner by default
        self.client.force_authenticate(user=self.user_owner)

    def test_create_project(self):
        # Ensure this is the correct name as defined in your urls.py
        url = reverse('projects-list')
        data = {'name': 'New Project', 'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming 3 "Unassigned" projects + 1 in setUp + 1 newly created = 5
        self.assertEqual(Project.objects.count(), 5)

    def test_list_projects(self):
        # Make sure to correctly set the expected number of public projects.
        # Assuming you want to verify the listing includes only public projects viewable by `self.user_non_member`.
        self.project.is_public = True
        self.project.save()

        self.client.force_authenticate(user=self.user_non_member)
        # Make sure this name matches your URL name for listing projects.
        url = reverse('projects-list')
        response = self.client.get(url)

        # Calculate the expected number of public projects.
        # If there's only one public project (`self.project`), expecting `1` makes sense.
        expected_public_projects_count = Project.objects.filter(
            is_public=True).count()

        # Adjust expectation based on actual setup.
        self.assertEqual(len(response.data), expected_public_projects_count)

    def test_add_user_to_project(self):
        url = reverse('projects-add-user', args=[self.project.pk])
        data = {'user_id': self.user_member.pk, 'role': 'Member'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProjectMembership.objects.filter(
            project=self.project, user=self.user_member).exists())

    def test_remove_user_from_project(self):
        # First, add a user to set up the test
        ProjectMembership.objects.create(
            project=self.project, user=self.user_member, role='Member')

        url = reverse('projects-remove-user', args=[self.project.pk])
        data = {'user_id': self.user_member.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProjectMembership.objects.filter(
            project=self.project, user=self.user_member).exists())

    def test_set_user_role(self):
        # First, add a user to set up the test
        ProjectMembership.objects.create(
            project=self.project, user=self.user_member, role='Viewer')

        url = reverse('projects-set-user-role', args=[self.project.pk])
        data = {'user_id': self.user_member.pk, 'role': 'Project Manager'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProjectMembership.objects.get(
            project=self.project, user=self.user_member).role, 'Project Manager')


class PublicProjectsListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        # Create a user
        cls.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Create public and private projects
        Project.objects.create(name='Public Project 1',
                               is_public=True, owner=cls.user)
        Project.objects.create(name='Public Project 2',
                               is_public=True, owner=cls.user)
        Project.objects.create(name='Private Project',
                               is_public=False, owner=cls.user)

    def test_list_public_projects(self):
        """
        Ensure the public projects endpoint only returns public projects.
        """
        url = reverse('public-projects')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for project in response.data['results']:  # Adjusted for pagination
            self.assertTrue(project['is_public'],
                            "Only public projects should be returned.")

    def test_pagination(self):
        """
        Test that the public projects endpoint correctly paginates the results.
        """
        url = reverse('public-projects')
        response = self.client.get(url)

        # Assuming your pagination setting is set to paginate after 10 items
        page_size = 10  # Use the actual page size used in your pagination class

        total_public_projects = Project.objects.filter(is_public=True).count()

        if total_public_projects > page_size:
            self.assertIsNotNone(
                response.data['next'], "Should have a next page.")
        else:
            self.assertIsNone(
                response.data['next'], "Should not have a next page.")
            self.assertIsNone(
                response.data['previous'], "Should not have a previous page.")
