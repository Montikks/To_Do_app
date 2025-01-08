from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from tasks.forms import TaskForm, SubtaskForm

class TaskFormTestCase(TestCase):
    def test_valid_task_form(self):
        """Zadáváme platná data, formulář by měl být validní."""
        form_data = {
            'name': 'Valid Task',
            'description': 'Popis',
            'completed': False,
            'deadline': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
            'notification_time': 24
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_deadline(self):
        """Deadline v minulosti -> nevalidní."""
        form_data = {
            'name': 'Bad Deadline Task',
            'deadline': (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'notification_time': 24
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('deadline', form.errors)

    def test_invalid_notification_time(self):
        """Notifikační čas mimo [1,72] -> nevalidní."""
        form_data = {
            'name': 'OutOfRange NotifTime',
            'deadline': (timezone.now() + timedelta(hours=10)).strftime('%Y-%m-%dT%H:%M'),
            'notification_time': 999  # Třeba moc velké
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('notification_time', form.errors)


class SubtaskFormTestCase(TestCase):
    def test_subtask_form_valid(self):
        """SubtaskForm by měl být validní s jedním povinným polem 'name'."""
        form_data = {'name': 'Some Subtask'}
        form = SubtaskForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_subtask_form_empty(self):
        """Pokus o prázdný subtask - nevalidní."""
        form_data = {}
        form = SubtaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
