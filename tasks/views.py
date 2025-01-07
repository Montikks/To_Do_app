from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Subtask
from .forms import TaskForm, SubtaskForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta


@login_required
def task_list(request):
    filter_status = request.GET.get('status', '')
    filter_deadline = request.GET.get('deadline', '')
    sort_option = request.GET.get('sort', '')
    search_query = request.GET.get('search', '')

    tasks = Task.objects.filter(user=request.user)

    # Filtrování podle stavu
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    # Filtrování podle termínu
    if filter_deadline == 'today':
        tasks = tasks.filter(deadline=timezone.now().date())
    elif filter_deadline == 'upcoming':
        tasks = tasks.filter(deadline__gt=timezone.now().date())
    elif filter_deadline == 'overdue':
        tasks = tasks.filter(deadline__lt=timezone.now().date(), completed=False)

    # Třídění
    if sort_option == 'deadline_asc':
        tasks = tasks.order_by('deadline')
    elif sort_option == 'deadline_desc':
        tasks = tasks.order_by('-deadline')
    elif sort_option == 'status':
        tasks = tasks.order_by('completed', 'deadline')
    elif sort_option == 'completion_asc':
        tasks = sorted(tasks, key=lambda t: t.completion_percentage())
    elif sort_option == 'completion_desc':
        tasks = sorted(tasks, key=lambda t: t.completion_percentage(), reverse=True)

    # Vyhledávání
    if search_query:
        tasks = tasks.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subtasks__name__icontains=search_query)
        ).distinct()

    # Logika pro rozdělení notifikací
    upcoming_notifications = []
    for task in tasks:
        if task.is_notification_due():
            time_diff = task.deadline - timezone.now()
            hours, remainder = divmod(time_diff.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            upcoming_notifications.append({
                'task': task,
                'hours': int(hours),
                'minutes': int(minutes)
            })

    overdue_notifications = tasks.filter(deadline__lt=timezone.now(), completed=False)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'filter_status': filter_status,
        'filter_deadline': filter_deadline,
        'sort_option': sort_option,
        'search_query': search_query,
        'upcoming_notifications': upcoming_notifications,
        'overdue_notifications': overdue_notifications,
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
    subtasks = task.subtasks.all()
    return render(request, 'tasks/task_detail.html', {'task': task, 'subtasks': subtasks})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('task_list')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')


@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed=True)
    return render(request, 'tasks/completed_tasks.html', {'tasks': tasks})


@login_required
def pending_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed=False)
    return render(request, 'tasks/pending_tasks.html', {'tasks': tasks})


@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
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
    subtask = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
    subtask.completed = True
    subtask.save()
    return redirect('task_detail', task_id=task_id)


@login_required
def edit_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
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
    subtask = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
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
