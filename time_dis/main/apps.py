from django.apps import AppConfig
from django.conf import settings


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from time_dis import operator
            operator.start()
