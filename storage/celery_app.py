import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storage.settings')

app = Celery('storage')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'daily-check-overdue-orders': {
        'task': 'storage.tasks.check_overdue_orders',
        'schedule': 86400,
    },
}
