from datetime import timedelta, date, datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.timezone import localdate
from django.views.generic import RedirectView, TemplateView

from .forms import TransferForm
from .models import TasksProgress
from auth_app.models import Users
from tasks_app.models import Tasks, Subtasks
import calendar
from .utils import Calendar


def reload_progress():
    cur_date = localdate()
    if cur_date.month == 1 and cur_date.day == 1:
        # Year reload
        TasksProgress.objects.filter(progress_range='YEAR').delete()
    if cur_date.day == 1:
        # Month reload
        TasksProgress.objects.filter(progress_range='MONTH').delete()
    TasksProgress.objects.filter(progress_range='WEEK').delete()
    print('Прогресс пользователей был обновлён')


def daily_send_messages():
    mail_data = ()
    users = Users.objects.all()
    for user in users:
        tasks = user.tasks.filter(deadline__date=localdate()).values('title').all()
        if len(tasks) != 0:
            message = f"Ваши задачи на сегодняшний день:\n{', '.join([task.get('title') for task in tasks])}" \
                      f"\nПодробнее о ваших задачах можете узнать здесь: http://127.0.0.1:8000/"
            mail_data += ('Задачи на сегодняшний день', message, settings.EMAIL_HOST_USER, [user.email]),
    send_mass_mail(mail_data, fail_silently=False)
    print('Ежедневная рассылка была выполнена')


@login_required
def main(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, instance=request.user.tasks.get(id=request.POST.get('transfer_task')))
        if form.is_valid():
            form.save()
        return redirect('main')
    daily = request.user.tasks.filter(deadline__date=localdate()).order_by('priority__title')\
        .select_related('category', 'priority').all()
    daily_fin = request.user.tasks.filter(Q(deadline__date=localdate()) &
                                          Q(progress=1)).order_by('priority__title')\
        .select_related('category', 'priority').all()
    daily_not_fin = request.user.tasks.filter(Q(deadline__date=localdate()) &
                                              Q(progress=0)).order_by('priority__title')\
        .select_related('category', 'priority').all()
    if len(daily) > 0:
        pb_data = int((len(daily_fin)-0)*100/(len(daily)-0))
    else:
        pb_data = 100
    form = TransferForm()

    chart_queryset = request.user.task_progress.order_by('task_finished').all()
    chart_labels = [item.category_name for item in chart_queryset]
    chart_data = [item.task_finished for item in chart_queryset]
    return render(request, 'main/main_menu.html', {'daily': daily, 'daily1': daily_fin,
                                                   'daily2': daily_not_fin, 'pb_data': pb_data,
                                                   'form': form, 'chart_labels': chart_labels,
                                                   'chart_data': chart_data, 'chart_queryset': chart_queryset})


class SuccessTaskView(RedirectView):
    url = reverse_lazy('main')

    def get(self, request, *args, **kwargs):
        success_task = get_object_or_404(Tasks, pk=request.GET.get('task_pk'))
        success_task.progress = 1
        success_task.save()

        success_subtasks = success_task.subtasks.all()
        if success_subtasks.exists():
            updated_subtasks = list()
            for subtask in success_subtasks:
                subtask.progress = 1
                updated_subtasks.append(subtask)
            Subtasks.objects.bulk_update(updated_subtasks, ['progress'])

        updated_progress = list()
        for progress_range, _ in TasksProgress.PROGRESS_RANGE:
            t_progress, _ = TasksProgress.objects.get_or_create(
                user=request.user,
                category_name=success_task.category.title,
                progress_range=progress_range,
                defaults={'task_finished': 0}
            )
            t_progress.task_finished = F('task_finished') + 1
            updated_progress.append(t_progress)
        if updated_progress:
            TasksProgress.objects.bulk_update(updated_progress, ['task_finished'])
        return super(SuccessTaskView, self).get(request, *args, **kwargs)


class SuccessSubtaskView(RedirectView):
    url = reverse_lazy('main')

    def get(self, request, *args, **kwargs):
        subtask = get_object_or_404(Subtasks, pk=request.GET.get('subtask_pk'))
        subtask.progress = 1
        subtask.save()
        return super(SuccessSubtaskView, self).get(request, *args, **kwargs)


class CalendarView(TemplateView):
    template_name = 'main/task_calendar.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        month = self.request.GET.get('month', None)
        y, m = d.year, d.month
        if month:
            y, m = list(map(int, month.split('-')))
        cal = Calendar(y, m, self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['task_calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month_value = first - timedelta(days=1)
    return 'month=' + str(prev_month_value.year) + '-' + str(prev_month_value.month)


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month_value = last + timedelta(days=1)
    return 'month=' + str(next_month_value.year) + '-' + str(next_month_value.month)
