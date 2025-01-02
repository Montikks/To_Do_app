from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def completion_percentage(self):
        total = self.subtasks.count()
        if total == 0:
            # Pokud nemáme podúkoly, úkol je buď 0% nebo 100% podle toho, zda je jako celek splněný
            return 100 if self.completed else 0
        done = self.subtasks.filter(completed=True).count()
        return int((done / total) * 100)

class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Subtask of {self.task.name})"
