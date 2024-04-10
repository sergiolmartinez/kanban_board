# tasks/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Task
from projects.models import Project


class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='autotestuser', email='user@test.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            name='Test Project', owner=self.user)
        self.task = Task.objects.create(
            title='Test Task', description='Test Task Description', owner=self.user, project=self.project)

        self.create_url = reverse('task-list')

    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'New Task Description',
                'project': self.project.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.latest('id').title, 'New Task')

    def test_list_tasks(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming pagination is not set up
        self.assertEqual(len(response.data), 1)

    def test_retrieve_task(self):
        detail_url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        detail_url = reverse('task-detail', args=[self.task.id])
        data = {'title': 'Updated Task',
                'description': 'Updated Task Description'}
        response = self.client.put(detail_url, data)
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        detail_url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
