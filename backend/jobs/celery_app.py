from celery import Celery
from celery.schedules import crontab

from config import Config

def make_celery(app):
    celery = Celery(
        app.import_name,
        include = ["jobs.daily_reminder", "jobs.monthly_report", "jobs.export_csv"]
    )
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone='Asia/Kolkata',
        enable_utc=True
    )
    celery.set_default()

    celery.conf.beat_schedule = {
        'daily-reminder': {
            'task': 'jobs.daily_reminder.send_daily_reminders',
            'schedule': crontab(hour = Config.DAILY_REMINDER_HOUR, minute = Config.DAILY_REMINDER_MINUTE)
        },
        'monthly-report': {
            'task': 'jobs.monthly_report.generate_monthly_report',
            'schedule': crontab(day_of_month = Config.MONTHLY_REPORT_DAY, hour = Config.MONTHLY_REPORT_HOUR, minute = Config.MONTHLY_REPORT_MINUTE)
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery