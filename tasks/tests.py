from django.test import TestCase
from .models import Task
from django.urls import reverse

class TaskModelsTestCast(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="Testovací úkol",
            description="Popis testovacího úkolu",
            completed=False,
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name,"Testovací úkol")
        self.assertEqual(self.task.description, "Popis testovacího úkolu")
        self.assertFalse(self.task.completed)

class TaskListViewTestCast(TestCase):
    def setUp(self):
        Task.objects.create(name="ukol 1", description="popis 1", completed=False)
        Task.objects.create(name="ukol 2", description="popis 2", completed=True)

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ukol 1")
        self.assertContains(response, "ukol 2")

class TaskViewTestCase(TestCase):
    def test_add_task(self):
        response = self.client.post(reverse("add_task"), {
            "name": "ukol 1",
            "description": "popis 1",
            "complete": False,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.last().name, "ukol 1")


