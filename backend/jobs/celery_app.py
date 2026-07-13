from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker = app.config['CELERY_BROKER_URL'],
        backend = app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        'daily-reminder': {
            'task': 'jobs.daily_reminder.send_daily_reminders',
            'schedule': crontab(hour = 12, minute = 0)
        },
        'monthly-report': {
            'task': 'jobs.monthly_report.generate_monthly_report',
            'schedule': crontab(day_of_month = 14, hour = 12, minute = 0)
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery