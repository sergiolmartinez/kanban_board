# tasks/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task
from datetime import date

User = get_user_model()


class TaskModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(
            username='autotestuser', password='testpassword')
        cls.project = Project.objects.create(
            name='Test Project', owner=cls.user)
        cls.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            project=cls.project,
            owner=cls.user,
            status='TODO',
            priority=2,
            deadline=date.today()
        )

    def test_task_fields(self):
        # Test all field values
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.owner, self.user)
        self.assertEqual(self.task.status, 'TODO')
        self.assertEqual(self.task.priority, 2)
        self.assertEqual(self.task.deadline, date.today())

    def test_task_str(self):
        # Test the string representation
        self.assertEqual(str(self.task), 'Test Task')
