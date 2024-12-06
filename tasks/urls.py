from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add_task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('completed_tasks/', views.completed_tasks, name='complete_tasks'),
    path('pending_tasks/', views.pending_tasks, name='pending_tasks'),
    path('task/<int:task_id>/add_subtask/', views.add_subtask, name='add_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/complete/', views.complete_subtask, name='complete_subtask'),
]
