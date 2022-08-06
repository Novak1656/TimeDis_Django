from django.urls import path
from .views import *

urlpatterns = [
    path('add_task/', add_task, name='add_task'),
    path('my_tasks/', TaskList.as_view(), name='my_tasks'),
    path('delete_task/<str:slug>', delete_task, name='delete_task'),
    path('task/<str:slug>', TaskDetail.as_view(), name='task'),
    path('update_task/<str:slug>', update_task, name='update_task'),
    path('my_tasks/search/', TaskSearch.as_view(), name='task_search'),
    path('my_tasks/<str:category>', tasks_by_category, name='tasks_by_category'),
]
