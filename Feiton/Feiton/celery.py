#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Feiton.settings')
# temperory, should not do that at production
os.environ.setdefault('C_FORCE_ROOT', 'true')

from django.conf import settings  # noqa

app = Celery('Feiton')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
