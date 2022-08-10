from django.contrib import admin
from .models import Tasks, Categories, Priority


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'category', 'priority', 'user', 'deadline', 'created_on', 'progress',)
    list_filter = ('category', 'title', 'priority', 'user', 'created_on', 'deadline',)
    search_fields = ('title',)
    list_display_links = ('id', 'slug', 'title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Categories, Priority)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_display_links = ('id', 'title',)


admin.site.register(Tasks, TasksAdmin)
