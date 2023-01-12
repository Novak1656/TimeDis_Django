from django.contrib import admin
from .models import Tasks, Categories, Priority, Subtasks


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'category', 'priority', 'remind_type', 'user', 'deadline', 'created_on',
                    'progress', 'failed',)
    list_filter = ('category', 'priority', 'failed', 'remind_type',)
    search_fields = ('title',)
    list_display_links = ('id', 'slug', 'title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Categories, Priority)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)
    list_display_links = ('id', 'title',)


@admin.register(Subtasks)
class SubtasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'title', 'progress',)
    list_filter = ('progress',)
    search_fields = ('title',)
    list_display_links = ('id', 'title',)
