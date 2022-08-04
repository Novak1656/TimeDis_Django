from django.db import models
from auth_app.models import Users


class Categories(models.Model):
    title = models.CharField('Название', max_length=250)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Priority(models.Model):
    title = models.CharField('Название', max_length=250)

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'
        ordering = ['title']

    def __str__(self):
        return self.title


class Tasks(models.Model):
    title = models.CharField('Название', max_length=250)
    comment = models.TextField('Подробности', blank=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='tasks')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name='tasks')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='tasks')
    deadline = models.DateTimeField('Срок выполнения', blank=True, null=True)
    created_on = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_on = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user}: {self.title}"


'''
class Reminds(models.Model):
---- 
'''