from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_unix.settings")

app = Celery("backend_unix")

# Configure Celery using Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks from all registered Django app configs.
app.autodiscover_tasks()
