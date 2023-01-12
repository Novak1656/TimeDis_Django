from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('daily/task/success', SuccessTaskView.as_view(), name='task_success'),
    path('daily/subtask/success', SuccessSubtaskView.as_view(), name='subtask_success'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('my_progress/', TasksProgressView.as_view(), name='my_progress'),
]
