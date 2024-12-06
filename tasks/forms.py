from django import forms
from .models import Task, Subtask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'completed']

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['name']
