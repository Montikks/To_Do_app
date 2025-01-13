# tasks/forms.py
from django import forms
from .models import Task, Subtask


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Termín (včetně času)"
    )
    notification_time = forms.IntegerField(
        min_value=1,
        max_value=72,  # ladí s validate_notification_time
        initial=24,
        label="Notifikace (hodiny před termínem)",
        help_text="Kolik hodin před termínem má být odeslána notifikace."
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'completed', 'deadline', 'notification_time']


class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['name']
