from django import forms
from .models import Task, Subtask, Template, SubtaskTemplate


# Formulář pro šablonu úkolu
class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'description', 'repeat_interval']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název šablony'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Popis šablony'}),
            'repeat_interval': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Template.objects.filter(name=name).exists():
            raise forms.ValidationError("Šablona s tímto názvem již existuje.")
        return name


# Formulář pro podúkoly šablony
class SubtaskTemplateForm(forms.ModelForm):
    class Meta:
        model = SubtaskTemplate
        fields = ['name', 'description']  # ✅ Přidán popis
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název podúkolu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Popis podúkolu', 'rows': 3}),  # ✅ Popis
        }


    class Meta:
        model = SubtaskTemplate
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název podúkolu'}),
        }


# Formulář pro běžný úkol
class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Termín (včetně času)"
    )
    notification_time = forms.IntegerField(
        min_value=1,
        max_value=72,
        initial=24,
        label="Notifikace (hodiny před termínem)",
        help_text="Kolik hodin před termínem má být odeslána notifikace."
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'completed', 'deadline', 'notification_time']


# Formulář pro běžný podúkol
class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název podúkolu'}),
        }
