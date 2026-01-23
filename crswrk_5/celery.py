from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crswrk_5.settings")

app = Celery("crswrk_5")

app.config_from_object("crswrk_5.settings", namespace="CELERY")

app.autodiscover_tasks()