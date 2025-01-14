from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Template(models.Model):
    name = models.CharField(max_length=255, verbose_name="Název šablony")
    description = models.TextField(blank=True, verbose_name="Popis šablony")
    repeat_interval = models.CharField(
        max_length=20,
        choices=[
            ('none', 'Neopakovat'),
            ('daily', 'Denně'),
            ('weekly', 'Měsíčně')
        ],
        default='none',
        verbose_name="Interval opakování"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vytvořil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vytvořeno")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualizováno")

    def __str__(self):
        return self.name


def validate_notification_time(value):
    if value < 1 or value > 72:
        raise ValidationError("Notifikační čas musí být mezi 1 a 72 hodinami.")


def validate_deadline(value):
    if value < now():
        raise ValidationError("Termín musí být v budoucnosti.")


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(
        null=True, blank=True,
        validators=[validate_deadline]
    )
    notification_time = models.PositiveIntegerField(
        default=24,
        validators=[validate_notification_time],
        help_text="Počet hodin před termínem, kdy má být odeslána notifikace."
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def completion_percentage(self):
        total = self.subtasks.count()
        if total == 0:
            return 100 if self.completed else 0
        done = self.subtasks.filter(completed=True).count()
        return int((done / total) * 100)

    def get_time_until_deadline(self):
        if not self.deadline:
            return None
        time_diff = self.deadline - now()
        if time_diff.total_seconds() > 0:
            hours, remainder = divmod(time_diff.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            return int(hours), int(minutes)
        return None

    def is_notification_due(self):
        if not self.deadline or self.notification_time is None:
            return False
        current_time = now()
        notification_threshold = self.deadline - timedelta(hours=self.notification_time)
        return notification_threshold <= current_time <= self.deadline


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Subtask of {self.task.name})"
