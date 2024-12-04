from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm


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
    return render(request, 'tasks/task_detail.html', {'task': task})


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
