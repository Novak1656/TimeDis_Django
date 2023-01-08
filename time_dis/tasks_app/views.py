from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, CreateView
from .models import Tasks, Subtasks
from .forms import TasksForm, SubtasksForm
from django.db.models import Q
from django.core.paginator import Paginator


def chek_failed_tasks():
    tasks = Tasks.objects.filter(deadline__date__lt=now().date()).all()
    for task in tasks:
        if task.progress == 1:
            task.delete()
        else:
            task.failed = 1
            task.save()
    print('Проверка устаревших задач прошла успешно')


class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'
    extra_context = {'title': 'задачи', 'url_name': reverse_lazy('my_tasks')}
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
    extra_context = {'url_name': reverse_lazy('task_search')}
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
            if 'add_subtask' in request.POST:
                return redirect('add_subtask', task_pk=task.pk)
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


class SubtaskCreateView(AccessMixin, CreateView):
    model = Subtasks
    template_name = 'tasks_app/subtask_create.html'
    form_class = SubtasksForm
    login_url = reverse_lazy('login')

    def get_success_url(self):
        if 'create_finish' in self.request.POST:
            return reverse('my_tasks')
        return reverse('add_subtask', kwargs={'task_pk': self.kwargs.get('task_pk')})

    def form_valid(self, form):
        subtask = form.save(commit=False)
        task = Tasks.objects.get(pk=self.kwargs.get('task_pk'))
        subtask.task = task
        subtask.save()
        return super(SubtaskCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SubtaskCreateView, self).get_context_data(**kwargs)
        context['task_pk'] = self.kwargs.get('task_pk')
        return context
