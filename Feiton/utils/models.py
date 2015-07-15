#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Duoshuoattr(models.Model):
    since_id = models.BigIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
