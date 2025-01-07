from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add_task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('pending_tasks/', views.pending_tasks, name='pending_tasks'),
    path('task/<int:task_id>/add_subtask/', views.add_subtask, name='add_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/complete/', views.complete_subtask, name='complete_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/edit/', views.edit_subtask, name='edit_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/delete/', views.delete_subtask, name='delete_subtask'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),






    # Auth
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
]
