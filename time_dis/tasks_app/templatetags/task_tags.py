from django import template
from ..models import Categories, Priority
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.http import urlencode

register = template.Library()


@register.inclusion_tag('tasks_app/category_list.html')
def get_categories(user):
    categories = Categories.objects.annotate(cnt=Count('tasks', distinct=True)).filter(Q(tasks__user=user)
                                                                                       & Q(cnt__gt=0))
    return {'categories': categories}


@register.inclusion_tag('tasks_app/priority_list.html')
def get_priorities(user):
    priorities = Priority.objects.filter(tasks__user=user).annotate(cnt=Count('tasks', distinct=True))
    return {'priorities': priorities}


@register.inclusion_tag('tasks_app/filters_list.html')
def get_filters(url_name, cur_filter=None, search_attrs=None):
    if url_name == 'my_tasks':
        url = reverse('my_tasks')
    else:
        url = '{}?{}'.format(reverse(url_name), urlencode({'search_word': search_attrs}))
    data = {'url': url, 'filter_by': cur_filter, 'filers_list': [('title', 'По названию'),
                                                                 ('created_on', 'По дате создания'),
                                                                 ('deadline', 'По сроку выполнения')]}
    return data
