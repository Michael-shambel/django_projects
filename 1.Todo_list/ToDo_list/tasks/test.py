from django.test import TestCase
from .models import Task
from .serializers import TaskSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase



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

class TaskViewsTest(APITestCase):
    def setUp(self):
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'is_completed': False
        }
        self.task = Task.objects.create(**self.task_data)
    
    def test_list_tasks(self):
        url = reverse('task-list-create')
        response = self.client.get(url)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_create_task(self):
        url = reverse('task-list-create')
        new_task_data = {
            'title': 'New task',
            'description': 'New Description',
            'is_completed': False
        }
        response = self.client.post(url, new_task_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(title='New task').description, 'New Description')
    
    def test_retrieve_task(self):
        url = reverse('task-retrieve-update-destroy', args=[self.task.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_data['title'])
    
    def test_update_task(self):
        url = reverse('task-retrieve-update-destroy', args=[self.task.id])
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'is_completed': True
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.is_completed, True)
    
    def test_delete_task(self):
        url = reverse('task-retrieve-update-destroy', args=[self.task.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_create_task_invalid_data(self):
        url = reverse('task-list-create')  # Make sure this matches your URL name
        invalid_data = {
            'title': '',  # Title should not be empty
            'description': 'Test Description'
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        