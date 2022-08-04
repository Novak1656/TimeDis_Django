from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Tasks
from .forms import TasksForm


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('my_tasks')
    else:
        form = TasksForm()
    return render(request, 'tasks_app/add_task.html', {'form': form})


class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user).all()
