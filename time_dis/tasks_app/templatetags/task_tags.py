from django import template
from ..models import Categories, Priority
from django.db.models import Count, Q, Sum
from django.urls import reverse
from django.utils.http import urlencode

register = template.Library()


@register.inclusion_tag('tasks_app/search_bar.html')
def search_task():
    url = reverse('task_search')
    return {'search_url': url}


@register.inclusion_tag('tasks_app/category_list.html')
def get_categories(user):
    categories = Categories.objects.annotate(cnt=Count('tasks', distinct=True)).filter(Q(tasks__user=user)
                                                                                       & Q(cnt__gt=0))
    return {'categories': categories, 'all_cnt': sum([elm.cnt for elm in categories])}


@register.inclusion_tag('tasks_app/priority_list.html')
def get_priorities(user):
    priorities = Priority.objects.filter(tasks__user=user).annotate(cnt=Count('tasks', distinct=True))
    return {'priorities': priorities, 'all_cnt': sum([elm.cnt for elm in priorities])}


@register.inclusion_tag('tasks_app/filters_list.html')
def get_filters(url, cur_filter=None, search_attrs=None):
    data = {'url': url, 'filter_by': cur_filter, 'search_attrs': search_attrs,
            'filers_list': [('title', 'По названию'), ('created_on', 'По дате создания'),
                            ('deadline', 'По сроку выполнения')]}
    return data
