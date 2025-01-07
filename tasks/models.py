from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError

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

    def is_notification_due(self):
        if not self.deadline or self.notification_time is None:
            return False
        current_time = now()
        notification_threshold = self.deadline - timedelta(hours=self.notification_time)
        return notification_threshold <= current_time <= self.deadline

    def __str__(self):
        return self.name

    def completion_percentage(self):
        total = self.subtasks.count()
        if total == 0:
            return 100 if self.completed else 0
        done = self.subtasks.filter(completed=True).count()
        return round((done / total) * 100, 2)

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Subtask of {self.task.name})"


def is_notification_due(self):
    if not self.deadline or self.notification_time is None:
        print(f"[DEBUG] Task '{self.name}' - Missing deadline or notification_time")
        return False

    current_time = now()
    notification_threshold = self.deadline - timedelta(hours=self.notification_time)
    print(f"[DEBUG] Task '{self.name}':")
    print(f"  Current time: {current_time}")
    print(f"  Notification threshold: {notification_threshold}")
    print(f"  Deadline: {self.deadline}")

    result = notification_threshold <= current_time <= self.deadline
    print(f"  Notification due: {result}")
    return result