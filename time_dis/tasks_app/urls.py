from django.urls import path
from .views import *

urlpatterns = [
    path('add_task/', add_task, name='add_task'),
    path('add_task/<int:task_pk>/subtask/', login_required(SubtaskCreateView.as_view()), name='add_subtask'),
    path('my_tasks/', TaskList.as_view(), name='my_tasks'),
    path('delete_task/<str:slug>', delete_task, name='delete_task'),
    path('task/<str:slug>', TaskDetail.as_view(), name='task'),
    path('update_task/<str:slug>', update_task, name='update_task'),
    path('my_tasks/search/', TaskSearch.as_view(), name='task_search'),
    path('my_tasks/category/<str:category>/', tasks_by_category, name='tasks_by_category'),
    path('my_tasks/priority/<str:priority>/', tasks_by_priority, name='tasks_by_priority'),
    path('task/<str:task_slug>/subtask/create/', login_required(NewSubtaskView.as_view()), name='new_subtask'),
    path(
        'task/<str:task_slug>/subtask/update/<int:pk>/',
        login_required(SubtaskUpdateView.as_view()),
        name='update_subtask'
    ),
    path(
        'task/<str:task_slug>/subtask/delete/<int:pk>/',
        login_required(SubtaskDeleteView.as_view()),
        name='delete_subtask'
    )
]
