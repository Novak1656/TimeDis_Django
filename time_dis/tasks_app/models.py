from django_unique_slugify import unique_slugify
from unidecode import unidecode
from django.db import models
from auth_app.models import Users
from django.urls import reverse
from django.utils.text import slugify


class Categories(models.Model):
    title = models.CharField('Название', max_length=250)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Priority(models.Model):
    title = models.CharField('Название', max_length=250, default='Важно-срочно')
    tag = models.CharField('Тег', max_length=100, default='danger')

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'
        ordering = ['title']

    def __str__(self):
        return self.title


class Tasks(models.Model):
    REMIND_TYPE = [('Never', 'Никогда'), ('OneTime', 'Один раз'), ('EveryDay', 'Каждый день')]

    slug = models.SlugField(max_length=250, null=True, allow_unicode=True)
    title = models.CharField('Название', max_length=250)
    comment = models.TextField('Подробности', blank=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='tasks', verbose_name='Категория')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name='tasks', verbose_name='Приоритет')
    remind_type = models.CharField(verbose_name='Напоминать', max_length=20, default='OneTime')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='tasks')
    progress = models.BooleanField('Прогресс', default=0)
    deadline = models.DateTimeField('Срок выполнения', blank=True, null=True)
    created_on = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_on = models.DateTimeField('Дата изменения', auto_now=True)
    failed = models.BooleanField('Просрочено', default=0)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(Tasks, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('task', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.user}: {self.title}"


class Subtasks(models.Model):
    task = models.ForeignKey(
        verbose_name='Задача',
        to=Tasks,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    comment = models.TextField(
        verbose_name='Подробности',
        blank=True
    )
    progress = models.BooleanField(
        'Прогресс',
        default=0
    )

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'
        ordering = ['title']

    def __str__(self):
        return self.title
