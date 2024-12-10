from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task, Subtask

class TasksTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.task = Task.objects.create(user=self.user, name="Test Task")

class TaskModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = Task.objects.create(
            user=self.user,
            name="Testovací úkol",
            description="Popis testovacího úkolu",
            completed=False,
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Testovací úkol")
        self.assertEqual(self.task.description, "Popis testovacího úkolu")
        self.assertFalse(self.task.completed)

class TaskListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        Task.objects.create(user=self.user, name="ukol 1")

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ukol 1")

class TaskViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_add_task(self):
        response = self.client.post(reverse("add_task"), {
            "name": "ukol 1",
            "description": "popis testovacího úkolu",
            "completed": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().name, "ukol 1")

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login(self):
        response = self.client.post(reverse("login"), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

class SubTaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.task = Task.objects.create(user=self.user, name="Main Task")

    def test_add_subtask(self):
        response = self.client.post(reverse("add_subtask", args=[self.task.id]), {'name': 'Test Subtask'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.subtasks.all().count(), 1)

    def test_complete_subtask(self):
        subtask = Subtask.objects.create(task=self.task, name="Test Subtask")
        response = self.client.get(reverse("complete_subtask", args=[self.task.id, subtask.id]))
        self.assertEqual(response.status_code, 302)
        subtask.refresh_from_db()
        self.assertTrue(subtask.completed)





















