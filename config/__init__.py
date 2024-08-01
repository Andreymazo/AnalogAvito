from __future__ import absolute_import, unicode_literals

# Это позволит убедиться, что приложение всегда импортируется, когда запускается Django
from config.celery import app as celery_app

__all__ = ('celery_app',)

# celery -A config worker -l info
# celery -A config beat -l info
# flower -A celery_django --port=5555
# celery -A tasks.app flower
#celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
#celery -A proj beat
#celery -A proj worker -B
# celery -A proj beat -s /home/celery/var/run/celerybeat-schedule
# celery -A your_project_name.celery beat --loglevel=info
#celery -A your_project_name worker --loglevel=info
# celery -A your_project_name beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
#$ celery -A proj purge
#celery -A config purge
# celery purge