from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from main.views import reload_week_progress, daily_send_messages


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', weeks=1, name='auto_reload_week_progress')
    def auto_reload_week_progress():
        reload_week_progress()

    @scheduler.scheduled_job('interval', days=1, name='auto_daily_send_messages')
    def auto_daily_send_messages():
        daily_send_messages()

    scheduler.start()
