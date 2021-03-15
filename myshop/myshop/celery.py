import os
from celery import Celery

# set default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
# celery will look for task.py files in each application to load async tasks.
app.autodiscover_tasks()