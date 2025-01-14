from django.urls import path
from . import views, auth_views

urlpatterns = [
    # Dashboard a AJAX hledání
    path('', views.dashboard_view, name='dashboard'),
    path('ajax_search/', views.ajax_search, name='ajax_search'),

    # Úkoly a podúkoly
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/add_subtask/', views.add_subtask, name='add_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/complete/', views.complete_subtask, name='complete_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/delete/', views.delete_subtask, name='delete_subtask'),
    path('task/<int:task_id>/subtask/<int:subtask_id>/edit/', views.edit_subtask, name='edit_subtask'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),

    # Šablony úkolů
    path('templates/', views.template_list, name='template_list'),  # Oprava názvu
    path('templates/create/', views.create_template, name='create_template'),
    path('templates/<int:template_id>/add_subtask/', views.add_subtask_to_template, name='add_subtask_to_template'),
    path('templates/<int:template_id>/edit/', views.edit_template, name='edit_template'),
    path('templates/<int:template_id>/delete/', views.delete_template, name='delete_template'),
    path('templates/<int:template_id>/generate_task/', views.generate_task_from_template, name='generate_task_from_template'),
    # Detail šablony
    path('templates/<int:template_id>/', views.template_detail, name='template_detail'),
    path('templates/subtask/<int:subtask_id>/delete/', views.delete_subtask_template, name='delete_subtask_template'),
    # URL pro detail podúkolu v šabloně
    path('templates/<int:template_id>/subtask/<int:subtask_id>/', views.subtask_template_detail, name='subtask_template_detail'),

    # Autentizace
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
]
