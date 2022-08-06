from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Tasks
from .forms import TasksForm
from django.db.models import Q


class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'
    extra_context = {'title': 'задачи', 'filers_list': [('title', 'По названию'),
                                                        ('created_on', 'По дате создания'),
                                                        ('deadline', 'По сроку выполнения')]}
    paginate_by = 2

    def filter_by(self, order):
        return Tasks.objects.filter(user=self.request.user).order_by(order).all()

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return self.filter_by(self.request.GET.get('filter_by'))
        return Tasks.objects.filter(user=self.request.user).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        if self.request.GET.get('filter_by'):
            context['filter_by'] = f"&filter_by={self.request.GET.get('filter_by')}"
        return context


class TaskSearch(LoginRequiredMixin, ListView):
    template_name = 'tasks_app/task_list_search.html'
    paginate_by = 2
    context_object_name = 'tasks'
    extra_context = {'filers_list': [('title', 'По названию'),
                                     ('created_on', 'По дате создания'),
                                     ('deadline', 'По сроку выполнения')]}
    # Проблемы с поиском кириллицы можно решить при переходе на PostgreSQL

    def filter_by(self, order):
        return Tasks.objects.filter(Q(user=self.request.user) &
                                    Q(title__icontains=self.request.GET.get('search_word'))).order_by(order).all()

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return self.filter_by(self.request.GET.get('filter_by'))
        return self.request.user.tasks.filter(title__icontains=self.request.GET.get('search_word')).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskSearch, self).get_context_data(**kwargs)
        context['search_word'] = f"search_word={self.request.GET.get('search_word')}"
        context['title'] = self.request.GET.get('search_word')
        if self.request.GET.get('filter_by'):
            context['filter_by'] = f"&filter_by={self.request.GET.get('filter_by')}"
        return context


def tasks_by_category(request, category):
    return render(request, '')


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks_app/task.html'
    context_object_name = 'task'

    def get_queryset(self):
        return self.request.user.tasks


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
