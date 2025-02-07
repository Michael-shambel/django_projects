from django.test import TestCase
from .models import Task
from .serializers import TaskSerializer

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

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.task_data = {
            'title': 'Test Task',
            'description': 'test description',
            'is_completed': False
        }
        self.task = Task.objects.create(**self.task_data)
        self.serializer = TaskSerializer(instance=self.task)
    
    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'updated_at']
        self.assertEqual(set(data.keys()), set(expected_fields))
    
    def test_serializer_data_matches_task(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.task_data['title'])
        self.assertEqual(data['description'], self.task_data['description'])
        self.assertEqual(data['is_completed'], self.task_data['is_completed'])
    
    def test_serializer_validation(self):
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())