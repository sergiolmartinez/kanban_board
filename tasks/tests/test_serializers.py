from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from tasks.models import Task
from tasks.serializers import TaskSerializer
from projects.models import Project

User = get_user_model()


class TaskSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='autotestuser', email='user@test.com', password='testpass123')
        self.project = Project.objects.create(
            name='Test Project', owner=self.user)

        # Setup request context for serializer
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'project': self.project.id,  # Pass the project ID for serializer input
            'status': 'TODO',
            'priority': 1
        }

    def test_create_task_with_owner_set_automatically(self):
        serializer = TaskSerializer(data=self.task_data, context={
                                    'request': self.request})
        self.assertTrue(serializer.is_valid())

        task = serializer.save()
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.owner, self.user)

    def test_serialize_task_data(self):
        task = Task.objects.create(title='Test Task', description='Test Description',
                                   project=self.project, owner=self.user, status='TODO', priority=1)
        serializer = TaskSerializer(task)

        self.assertEqual(serializer.data['owner'], self.user.id)
        self.assertEqual(serializer.data['title'], 'Test Task')

    def test_disallow_direct_manipulation_of_owner_field(self):
        another_user = User.objects.create_user(
            username='anotheruser', password='password123')
        task_data_with_owner = self.task_data.copy()
        # Attempt to directly manipulate owner
        task_data_with_owner['owner'] = another_user.id

        serializer = TaskSerializer(data=task_data_with_owner, context={
                                    'request': self.request})
        self.assertTrue(serializer.is_valid())

        task = serializer.save()
        self.assertNotEqual(task.owner, another_user)
        self.assertEqual(task.owner, self.user)
