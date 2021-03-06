from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_courses.settings")

app = Celery("django_courses")
app.conf.task_default_queue = 'lowpriorityqueue'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
