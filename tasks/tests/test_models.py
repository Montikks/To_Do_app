from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from tasks.models import Task, Subtask


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(
            name="Test Task",
            description="Nějaký popis",
            completed=False,
            deadline=timezone.now() + timedelta(hours=24),
            notification_time=24,
            user=self.user
        )

    def test_completion_percentage_no_subtasks(self):
        """Úkol bez podúkolů: 100% pokud completed=True, jinak 0%."""
        self.assertEqual(self.task.subtasks.count(), 0)
        self.assertEqual(self.task.completion_percentage(), 0)

        self.task.completed = True
        self.task.save()
        self.assertEqual(self.task.completion_percentage(), 100)

    def test_completion_percentage_with_subtasks(self):
        """Zkontroluje, zda se procenta správně zaokrouhlují a počítají s ohledem na subtasky."""
        subtask1 = Subtask.objects.create(task=self.task, name='Subtask 1', completed=False)
        subtask2 = Subtask.objects.create(task=self.task, name='Subtask 2', completed=False)
        # Teď jsou 2 subtasky, oba nesplněné: 0%
        self.assertEqual(self.task.completion_percentage(), 0)

        subtask1.completed = True
        subtask1.save()
        # 1/2 = 50%
        self.assertEqual(self.task.completion_percentage(), 50)

        subtask2.completed = True
        subtask2.save()
        # 2/2 = 100%
        self.assertEqual(self.task.completion_percentage(), 100)

    def test_is_notification_due_true(self):
        """Notifikace by měla být due (true), pokud jsme v intervalu [deadline - notif, deadline]."""
        self.assertTrue(self.task.is_notification_due())

    def test_is_notification_due_false_after_deadline(self):
        """Posunout deadline do minulosti -> notifikace je False."""
        self.task.deadline = timezone.now() - timedelta(hours=1)
        self.task.save()
        self.assertFalse(self.task.is_notification_due())

    def test_str_task(self):
        """Kontrola __str__ u Task."""
        self.assertIn("Test Task", str(self.task))


class SubtaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.task = Task.objects.create(name="Parent Task", user=self.user)
        self.subtask = Subtask.objects.create(task=self.task, name="Child Subtask")

    def test_subtask_str(self):
        """Kontrola __str__ u Subtask."""
        self.assertIn("Child Subtask", str(self.subtask))
        self.assertIn("Parent Task", str(self.subtask))
