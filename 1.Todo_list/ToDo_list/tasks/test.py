from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            is_completed=False
        )
    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertFalse(self.task.is_completed)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
    
    def test_mark_task_completed(self):
        self.task.is_completed = True
        self.task.save()

        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
