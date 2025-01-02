from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Subtask
from .forms import TaskForm, SubtaskForm
from django.contrib.auth.decorators import login_required
from datetime import date


@login_required
def task_list(request):
    filter_status = request.GET.get('status', '')
    filter_deadline = request.GET.get('deadline', '')

    tasks = Task.objects.filter(user=request.user)

    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    if filter_deadline == 'today':
        tasks = tasks.filter(deadline=date.today())
    elif filter_deadline == 'upcoming':
        tasks = tasks.filter(deadline__gt=date.today())
    elif filter_deadline == 'overdue':
        tasks = tasks.filter(deadline__lt=date.today(), completed=False)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'filter_status': filter_status,
        'filter_deadline': filter_deadline,
    })




@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})



@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    subtasks = task.subtasks.all()  # Díky related_name='subtasks' v modelu Subtask
    return render(request, 'tasks/task_detail.html', {'task': task, 'subtasks': subtasks})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

@login_required
def pending_tasks(request):
    tasks = Task.objects.filter(completed=False)
    return render(request, 'tasks/pending_tasks.html', {'tasks': tasks})

@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(completed=True)
    return render(request, 'tasks/completed_tasks.html', {'tasks': tasks})

@login_required
def add_subtask(request, task_id):
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

@login_required
def complete_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task_id=task_id)
    subtask.completed = True
    subtask.save()
    return redirect('task_detail', task_id=task_id)


@login_required
def edit_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task_id=task_id)
    if request.method == 'POST':
        form = SubtaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task_id)
    else:
        form = SubtaskForm(instance=subtask)
    return render(request, 'tasks/edit_subtask.html', {'form': form, 'task': subtask.task})


@login_required
def delete_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task_id=task_id)
    subtask.delete()
    return redirect('task_detail', task_id=task_id)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})
