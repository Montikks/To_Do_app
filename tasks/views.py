from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from .models import Task, Subtask, Template
from .forms import TaskForm, SubtaskForm, TemplateForm


# Seznam všech šablon
@login_required
def template_list(request):
    templates = Template.objects.all()
    return render(request, 'tasks/template_list.html', {'templates': templates})


# Vytvoření nové šablony
@login_required
def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('template_list')
    else:
        form = TemplateForm()
    return render(request, 'task/create_template.html', {'form': form})


@login_required
def dashboard_view(request):
    filter_status = request.GET.get('status', '')
    filter_deadline = request.GET.get('deadline', '')
    sort_option = request.GET.get('sort', '')
    search_query = request.GET.get('search', '')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user)
    now_time = timezone.now()

    # Filtrování stavu
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    # Filtrování termínu
    if filter_deadline == 'today':
        tasks = tasks.filter(deadline__date=now_time.date())
    elif filter_deadline == 'upcoming':
        tasks = tasks.filter(deadline__gt=now_time)
    elif filter_deadline == 'overdue':
        tasks = tasks.filter(deadline__lt=now_time, completed=False)

    # Řazení
    if sort_option == 'deadline_asc':
        tasks = tasks.order_by('deadline')
    elif sort_option == 'deadline_desc':
        tasks = tasks.order_by('-deadline')
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

    # Notifikace (toast)
    upcoming_notifications = []
    overdue_notifications = []
    for t in tasks:
        if t.is_notification_due():
            time_diff = t.deadline - now_time
            hours, remainder = divmod(time_diff.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            upcoming_notifications.append({
                'task': t,
                'hours': int(hours),
                'minutes': int(minutes)
            })
        if t.deadline and t.deadline < now_time and not t.completed:
            overdue_notifications.append(t)

    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,
        'form': form,
        'filter_status': filter_status,
        'filter_deadline': filter_deadline,
        'sort_option': sort_option,
        'search_query': search_query,
        'upcoming_notifications': upcoming_notifications,
        'overdue_notifications': overdue_notifications,
    })


@login_required
def ajax_search(request):
    query = request.GET.get('query', '').strip()
    tasks_qs = Task.objects.filter(user=request.user)
    if query:
        tasks_qs = tasks_qs.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(subtasks__name__icontains=query)
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
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'subtasks': task.subtasks.all(),
    })


@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = SubtaskForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.task = task
            sub.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = SubtaskForm()
    return render(request, 'tasks/add_subtask.html', {'task': task, 'form': form})


@login_required
def complete_subtask(request, task_id, subtask_id):
    sub = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
    sub.completed = True
    sub.save()
    return redirect('task_detail', task_id=task_id)


@login_required
def delete_subtask(request, task_id, subtask_id):
    sub = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
    sub.delete()
    return redirect('task_detail', task_id=task_id)


@login_required
def edit_subtask(request, task_id, subtask_id):
    sub = get_object_or_404(Subtask, id=subtask_id, task__id=task_id, task__user=request.user)
    if request.method == 'POST':
        form = SubtaskForm(request.POST, instance=sub)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task_id)
    else:
        form = SubtaskForm(instance=sub)
    return render(request, 'tasks/edit_subtask.html', {'form': form, 'task': sub.task})


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
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


# =============== KALENDÁŘ A POKROČILÉ NOTIFIKACE ===============


@login_required
def advanced_notifications_view(request):
    if request.method == 'POST':
        upcoming_tasks = Task.objects.filter(
            user=request.user,
            deadline__lte=timezone.now() + timedelta(hours=24),
            completed=False
        )
        if upcoming_tasks.exists():
            subject = "Blížící se termín úkolů"
            lines = ["Následující úkoly se blíží termínu:"]
            for ut in upcoming_tasks:
                lines.append(f"- {ut.name} (deadline: {ut.deadline:%d.%m.%Y %H:%M})")
            body = "\n".join(lines)
            send_mail(
                subject,
                body,
                None,
                [request.user.email or "test@console.local"],
                fail_silently=False
            )
            msg = "E-mail byl odeslán (mrkni do konzole)."
        else:
            msg = "Žádné úkoly s deadline do 24h."
        return render(request, 'tasks/advanced_notifications.html', {'message': msg})
    return render(request, 'tasks/advanced_notifications.html')
