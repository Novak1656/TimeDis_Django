from django.contrib import admin
from .models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_login', 'is_active']
    list_display_links = ['id', 'username']
    list_filter = ['username']
    search_fields = ['username']


admin.site.register(Users, UsersAdmin)
