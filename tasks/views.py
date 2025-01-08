# tasks/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from .models import Task, Subtask
from .forms import TaskForm, SubtaskForm

@login_required
def dashboard_view(request):
    """
    Stránka s taby:
      1) Seznam úkolů (v tabulce + hover subtasky)
      2) Filtry a vyhledávání
      3) Formulář pro přidání nového úkolu
    """
    filter_status = request.GET.get('status', '')
    filter_deadline = request.GET.get('deadline', '')
    sort_option = request.GET.get('sort', '')
    search_query = request.GET.get('search', '')

    if request.method == 'POST':
        # Form pro přidání úkolu
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    # Načteme úkoly
    tasks = Task.objects.filter(user=request.user)

    # Filtr status
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    # Filtr deadline
    now = timezone.now()
    if filter_deadline == 'today':
        tasks = tasks.filter(deadline__date=now.date())
    elif filter_deadline == 'upcoming':
        tasks = tasks.filter(deadline__gt=now)
    elif filter_deadline == 'overdue':
        tasks = tasks.filter(deadline__lt=now, completed=False)

    # Řazení
    if sort_option == 'deadline_asc':
        tasks = tasks.order_by('deadline')
    elif sort_option == 'deadline_desc':
        tasks = tasks.order_by('-deadline')
    elif sort_option == 'completion_asc':
        # sorted() - neuškodí, transformuje queryset na list
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

    # Notifikace
    upcoming_notifications = []
    overdue_notifications = []
    for t in tasks:
        if t.is_notification_due():
            time_diff = t.deadline - timezone.now()
            hours, remainder = divmod(time_diff.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            upcoming_notifications.append({
                'task': t,
                'hours': int(hours),
                'minutes': int(minutes)
            })
        if t.deadline and (t.deadline < timezone.now()) and not t.completed:
            overdue_notifications.append(t)

    context = {
        'tasks': tasks,
        'form': form,
        'filter_status': filter_status,
        'filter_deadline': filter_deadline,
        'sort_option': sort_option,
        'search_query': search_query,
        'upcoming_notifications': upcoming_notifications,
        'overdue_notifications': overdue_notifications,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def ajax_search(request):
    """
    AJAX endpoint pro dynamické vyhledávání (live search).
    Vrací JSON se seznamem úkolů (name, deadline, completed, atd.).
    """
    query = request.GET.get('query', '').strip()
    tasks_qs = Task.objects.filter(user=request.user)

    if query:
        tasks_qs = tasks_qs.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(subtasks__name__icontains=query)
        ).distinct()

    results = []
    for t in tasks_qs:
        results.append({
            'id': t.id,
            'name': t.name,
            'deadline': t.deadline.strftime('%d.%m.%Y %H:%M') if t.deadline else '',
            'completed': t.completed,
            'completion_percentage': t.completion_percentage(),
        })

    return JsonResponse({'tasks': results})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    subtasks = task.subtasks.all()
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'subtasks': subtasks,
    })


@login_required
def add_subtask(request, task_id):
    """
    Pohled pro přidání podúkolu k danému Task (task_id).
    """
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
    return render(request, 'tasks/add_subtask.html', {
        'form': form,
        'task': task,
    })


@login_required
def complete_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
    subtask.completed = True
    subtask.save()
    return redirect('task_detail', task_id=task_id)


@login_required
def delete_subtask(request, task_id, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
    subtask.delete()
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
    return render(request, 'tasks/edit_subtask.html', {
        'form': form,
        'task': subtask.task,
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('dashboard')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task,
    })
