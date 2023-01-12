from django.contrib import admin
from .models import TasksProgress


class TasksProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category_name', 'task_finished', 'task_failed', 'progress_range')
    list_display_links = ('id',)
    list_filter = ('category_name',)
    search_fields = ('user', 'category_name',)


admin.site.register(TasksProgress, TasksProgressAdmin)
