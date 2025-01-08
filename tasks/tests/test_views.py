from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from tasks.models import Task

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_dashboard_view_200(self):
        """Přihlášený uživatel -> dashboard by měl vracet 200 a používat tasks/dashboard.html."""
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/dashboard.html')

    def test_dashboard_requires_login(self):
        """Nepřihlášený -> redirect na login."""
        self.client.logout()
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class AddSubtaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(
            name="Main Task",
            deadline=timezone.now() + timedelta(days=1),
            notification_time=24,
            user=self.user
        )

    def test_add_subtask_post(self):
        """Po úspěšném POSTu by měl subtask vzniknout a vrátit detail úkolu."""
        url = reverse('add_subtask', args=[self.task.id])
        resp = self.client.post(url, data={'name': 'Nový podúkol'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        # Ověříme, že se subtask objevil v detailu
        self.assertContains(resp, 'Nový podúkol')
        self.assertTemplateUsed(resp, 'tasks/task_detail.html')
        self.assertEqual(self.task.subtasks.count(), 1)


class AjaxSearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(
            name="Searchable Task",
            user=self.user,
            deadline=timezone.now() + timedelta(days=1),
            notification_time=24
        )

    def test_ajax_search(self):
        """Ověří, že AJAX vyhledávání najde náš Task."""
        url = reverse('ajax_search')
        resp = self.client.get(url, {'query': 'Searchable'})
        self.assertEqual(resp.status_code, 200)
        json_data = resp.json()
        self.assertIn('tasks', json_data)
        tasks_list = json_data['tasks']
        self.assertEqual(len(tasks_list), 1)
        self.assertEqual(tasks_list[0]['name'], 'Searchable Task')
        self.assertIn('completion_percentage', tasks_list[0])
