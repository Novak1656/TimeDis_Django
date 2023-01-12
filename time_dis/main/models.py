from django.db import models
from auth_app.models import Users


class TasksProgress(models.Model):
    PROGRESS_RANGE = [('WEEK', 'За неделю'), ('MONTH', 'За месяц'), ('YEAR', 'За год')]

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=Users,
        on_delete=models.CASCADE,
        related_name='task_progress'
    )
    category_name = models.CharField(
        verbose_name='Категория',
        max_length=250
    )
    task_finished = models.IntegerField(
        verbose_name='Выполнено задач'
    )
    progress_range = models.CharField(
        verbose_name='Диапазон',
        max_length=15,
        default='WEEK'
    )

    class Meta:
        verbose_name = 'Прогресс по задачам'
        verbose_name_plural = 'Прогресс по задачам'
        ordering = ['user']

    def __str__(self):
        return f"{self.user.username}|{self.category_name}:{self.task_finished}"
