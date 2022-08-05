from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Tasks, Priority
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
    extra_context = {'title': 'задачи'}
    paginate_by = 5

    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user).all()


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks_app/task.html'
    context_object_name = 'task'

    def get_queryset(self):
        return self.request.user.tasks


@login_required
def update_task(request, slug):
    task = request.user.tasks.get(slug=slug)
    if request.method == 'POST':
        form = TasksForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('task', kwargs={'slug': slug}))
    else:
        form = TasksForm(instance=task)
    return render(request, 'tasks_app/update_task.html', {'form': form})


@login_required
def delete_task(request, slug):
    task = request.user.tasks.get(slug=slug)
    task.delete()
    return redirect('my_tasks')
