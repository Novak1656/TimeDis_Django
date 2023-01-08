from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('daily/task/success', SuccessTaskView.as_view(), name='task_success'),
    path('daily/subtask/success', SuccessSubtaskView.as_view(), name='subtask_success'),
]
