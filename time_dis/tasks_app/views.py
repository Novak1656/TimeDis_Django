from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Tasks
from .forms import TasksForm
from django.db.models import Q
from django.core.paginator import Paginator


class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'
    extra_context = {'title': 'задачи', 'url_name': reverse_lazy('my_tasks'),
                     'filers_list': [('title', 'По названию'),
                                     ('created_on', 'По дате создания'),
                                     ('deadline', 'По сроку выполнения')]}
    paginate_by = 10

    def filter_by(self, order):
        return Tasks.objects.filter(user=self.request.user).select_related('category', 'priority').order_by(order).all()

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return self.filter_by(self.request.GET.get('filter_by'))
        return Tasks.objects.filter(user=self.request.user).select_related('category', 'priority').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        if self.request.GET.get('filter_by'):
            context['filter_by'] = f"&filter_by={self.request.GET.get('filter_by')}"
        return context


class TaskSearch(LoginRequiredMixin, ListView):
    template_name = 'tasks_app/task_list_search.html'
    paginate_by = 10
    context_object_name = 'tasks'
    extra_context = {'url_name': reverse_lazy('task_search'), 'filers_list': [('title', 'По названию'),
                                                                         ('created_on', 'По дате создания'),
                                                                         ('deadline', 'По сроку выполнения')]}
    # Проблемы с поиском кириллицы можно решить при переходе на PostgreSQL

    def filter_by(self, order):
        return Tasks.objects.filter(Q(user=self.request.user) &
                                    Q(title__icontains=self.request.GET.get('search_word')))\
            .select_related('category', 'priority').order_by(order).all()

    def get_queryset(self):
        if self.request.GET.get('filter_by'):
            return self.filter_by(self.request.GET.get('filter_by'))
        return self.request.user.tasks.filter(title__icontains=self.request.GET.get('search_word'))\
            .select_related('category', 'priority').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskSearch, self).get_context_data(**kwargs)
        context['search_word'] = f"search_word={self.request.GET.get('search_word')}"
        context['title'] = self.request.GET.get('search_word')
        if self.request.GET.get('filter_by'):
            context['filter_by'] = f"&filter_by={self.request.GET.get('filter_by')}"
        return context


@login_required
def tasks_by_category(request, category):
    def filter_by(order):
        return request.user.tasks.filter(category__title=category).select_related('category', 'priority')\
            .order_by(order).all()
    data = {'title': f'задачи по категории: {category}', 'url_name': reverse_lazy('tasks_by_category', args=[category])}
    if request.GET.get('filter_by'):
        tasks = filter_by(request.GET.get('filter_by'))
        data['filter_by'] = f"&filter_by={request.GET.get('filter_by')}"
    else:
        tasks = request.user.tasks.filter(category__title=category).select_related('category', 'priority').all()
    page_obj = Paginator(tasks, 10).get_page(request.GET.get('page', 1))
    data['tasks'] = page_obj
    data['page_obj'] = page_obj
    return render(request, 'tasks_app/task_list.html', data)


@login_required
def tasks_by_priority(request, priority):
    def filter_by(order):
        return request.user.tasks.filter(priority__title=priority).select_related('category', 'priority')\
            .order_by(order).all()
    data = {'title': f'задачи по приоритету: {priority}',
            'url_name': reverse_lazy('tasks_by_priority', args=[priority])}
    if request.GET.get('filter_by'):
        tasks = filter_by(request.GET.get('filter_by'))
        data['filter_by'] = f"&filter_by={request.GET.get('filter_by')}"
    else:
        tasks = request.user.tasks.filter(priority__title=priority).select_related('category', 'priority').all()
    page_obj = Paginator(tasks, 10).get_page(request.GET.get('page', 1))
    data['page_obj'] = page_obj
    data['tasks'] = page_obj
    return render(request, 'tasks_app/task_list.html', data)


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
    if request.META['HTTP_REFERER'] == f"http://{request.META['HTTP_HOST']}/":
        return redirect('main')
    return redirect('my_tasks')
