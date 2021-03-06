from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tacticalrmm.settings")

app = Celery("tacticalrmm", backend="redis://" + settings.REDIS_HOST, broker="redis://" + settings.REDIS_HOST)
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.broker_url = "redis://" + settings.REDIS_HOST + ":6379"
app.result_backend = "redis://" + settings.REDIS_HOST + ":6379"
app.accept_content = ["application/json"]
app.result_serializer = "json"
app.task_serializer = "json"
app.conf.task_track_started = True
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-chocos': {
        'task': 'software.tasks.update_chocos',
        'schedule': crontab(minute=0, hour=4),
    },
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    from checks.tasks import (
        disk_check_alert,
        cpu_load_check_alert,
        mem_check_alert,
        win_service_check_task,
        checks_failing_task,
    )

    from core.models import CoreSettings

    interval = CoreSettings.objects.get(pk=1)

    sender.add_periodic_task(interval.disk_check_interval, disk_check_alert.s())
    sender.add_periodic_task(interval.cpuload_check_interval, cpu_load_check_alert.s())
    sender.add_periodic_task(interval.mem_check_interval, mem_check_alert.s())
    sender.add_periodic_task(interval.win_svc_check_interval, win_service_check_task.s())
    sender.add_periodic_task(30.0, checks_failing_task.s())
