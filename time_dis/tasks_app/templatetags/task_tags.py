from django import template
from django.utils.timezone import localtime

from ..models import Categories, Priority
from django.db.models import Count
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('tasks_app/search_bar.html')
def search_task():
    url = reverse('task_search')
    return {'search_url': url}


@register.inclusion_tag('tasks_app/category_list.html')
def get_categories(user):
    categories = Categories.objects.filter(tasks__user=user).annotate(cnt=Count('tasks', distinct=True))
    return {'categories': categories, 'all_cnt': sum([elm.cnt for elm in categories])}


@register.inclusion_tag('tasks_app/priority_list.html')
def get_priorities(user):
    priorities = Priority.objects.filter(tasks__user=user).annotate(cnt=Count('tasks', distinct=True))
    return {'priorities': priorities, 'all_cnt': sum([elm.cnt for elm in priorities])}


@register.inclusion_tag('tasks_app/filters_list.html')
def get_filters(url, cur_filter=None, search_attrs=None):
    data = {
        'url': url,
        'filter_by': cur_filter,
        'search_attrs': search_attrs,
        'filers_list': [
            ('title', 'По названию'),
            ('created_on', 'По дате создания'),
            ('deadline', 'По сроку выполнения'),
            ('-failed', 'По статусу'),
        ]
    }
    return data


@register.simple_tag
def get_subtasks_info(subtasks):
    unfinished_count = len(subtasks) - len(subtasks.filter(progress=0))
    return f'{unfinished_count}/{len(subtasks)}'


@register.inclusion_tag('tasks_app/striped_tasks_by_datetime.html')
def get_striped_tasks_by_datetime(tasks_list, stripe_type):
    tasks_queryset = tasks_list
    tasks_by_dates = {localtime(task.deadline).strftime("%d.%m.%Y"): list() for task in tasks_queryset if task.deadline}

    tasks_without_deadline = list()
    for task in tasks_queryset:
        if not task.deadline:
            tasks_without_deadline.append(task)
            continue
        task_date = localtime(task.deadline).strftime("%d.%m.%Y")
        tasks_by_dates[task_date].append(task)

    if stripe_type == 'date_stripe':
        return dict(tasks_list=tasks_by_dates, tasks_without_deadline=tasks_without_deadline)

    for date, tasks in tasks_by_dates.items():
        hours = [localtime(task.deadline).strftime("%H") for task in tasks]
        hours.sort()
        tasks_by_time = {hour: list() for hour in hours}
        for task in tasks:
            task_time = localtime(task.deadline).strftime("%H")
            tasks_by_time[task_time].append(task)
        tasks_by_dates[date] = tasks_by_time
    return dict(tasks_list=tasks_by_dates, tasks_without_deadline=tasks_without_deadline, striped_by=stripe_type)
