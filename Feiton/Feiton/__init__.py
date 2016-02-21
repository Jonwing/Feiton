# -*- coding: utf-8 -*-

from __future__ import absolute_import

# make sure celery app is always import when django starts
from .celery import app as celery_app  # noqa
