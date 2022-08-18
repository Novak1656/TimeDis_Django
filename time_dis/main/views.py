from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.shortcuts import render, redirect
from django.db.models import Q, F
from django.utils.timezone import now
from .forms import TransferForm
from .models import TasksProgress
from auth_app.models import Users


def reload_week_progress():
    TasksProgress.objects.all().delete()
    print('Еженедельный прогресс пользователей был обновлён')


def daily_send_messages():
    mail_data = ()
    users = Users.objects.all()
    for user in users:
        tasks = user.tasks.filter(deadline__date=now().date()).values('title').all()
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
    if request.GET.get('success'):
        success_task = request.user.tasks.get(id=request.GET.get('success'))
        success_task.progress = 1
        success_task.save()
        t_progress = request.user.task_progress.filter(category_name=success_task.category.title).first()
        if t_progress:
            t_progress.task_finished = F('task_finished') + 1
            t_progress.save()
            t_progress.refresh_from_db()
        else:
            TasksProgress.objects.create(user=request.user, category_name=success_task.category.title, task_finished=1)

        return redirect('main')
    daily = request.user.tasks.filter(deadline__date=now().date()).order_by('priority__title')\
        .select_related('category', 'priority').all()
    daily_fin = request.user.tasks.filter(Q(deadline__date=now().date()) &
                                          Q(progress=1)).order_by('priority__title')\
        .select_related('category', 'priority').all()
    daily_not_fin = request.user.tasks.filter(Q(deadline__date=now().date()) &
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


'''
Список работ:
- Ежедневная проверка на выявление просроченных задач
- Календарь
- Создание кастомных категорий для задач
'''