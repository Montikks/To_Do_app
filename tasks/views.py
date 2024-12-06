from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Subtask  # Přidáme i Subtask
from .forms import TaskForm, SubtaskForm  # Přidáme SubtaskForm

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    subtasks = task.subtasks.all()  # Díky related_name='subtasks' v modelu Subtask
    return render(request, 'tasks/task_detail.html', {'task': task, 'subtasks': subtasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

def pending_tasks(request):
    tasks = Task.objects.filter(completed=False)
    return render(request, 'tasks/pending_tasks.html', {'tasks': tasks})

def completed_tasks(request):
    tasks = Task.objects.filter(completed=True)
    return render(request, 'tasks/completed_tasks.html', {'tasks': tasks})

def add_subtask(request, task_id):
    # Nová view funkce pro přidání podúkolu
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = SubtaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = SubtaskForm()

    return render(request, 'tasks/add_subtask.html', {'form': form, 'task': task})


def complete_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task_id=task_id)
    subtask.completed = True
    subtask.save()
    return redirect('task_detail', task_id=task_id)