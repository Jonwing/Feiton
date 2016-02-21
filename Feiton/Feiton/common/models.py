# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from django.utils import timezone
from django.db import models


class RemoteIP(models.Model):
    ip = models.CharField(max_length=64)
    country = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'国家')
    area = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'区域')
    region = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'省份')
    city = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'城市')
    isp = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'运营商')
    accessed_at = models.DateTimeField(auto_now_add=True, verbose_name=u'访问时间')
    request_path = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'访问路径')

    save_interval = datetime.timedelta(0, 300)

    class Meta():
        verbose_name = u'来访记录'
        verbose_name_plural = u'来访记录'
        ordering = ['-pk']

    def __unicode__(self):
        return self.country + self.ip

    def save(self, *args, **kwargs):
        access_records = self.__class__.objects.filter(
            ip=self.ip,
            request_path=self.request_path)
        if access_records:
            last_access = access_records.first().accessed_at
            time_from_last_access = timezone.make_aware(
                                        datetime.datetime.now(),
                                        timezone.get_default_timezone()
                                        ) - last_access
            if time_from_last_access < self.save_interval:
                return

        return super(RemoteIP, self).save(*args, **kwargs)
