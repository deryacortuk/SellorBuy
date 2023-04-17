from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

import dotenv
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.read_dotenv(env_file)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SellorBuy.settings")
app = Celery("SellorBuy",broker='redis://redis:6379/0')
app.config_from_object("django.conf:settings",namespace="CELERY")
app.conf.enable_utc=True


app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)


