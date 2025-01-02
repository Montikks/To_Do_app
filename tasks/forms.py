from django import forms
from .models import Task, Subtask

class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Termín (včetně času)"
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'completed', 'deadline']

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['name']
