# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from django.db import models


# deprecated, will be removed some day
class RemoteIP(models.Model):
    ip = models.CharField(max_length=64, unique=True)
    country = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'国家')
    area = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'区域')
    region = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'省份')
    city = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'城市')
    isp = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'运营商')

    class Meta():
        verbose_name = u'ip信息'
        verbose_name_plural = u'ip信息'
        ordering = ['-pk']

    def __unicode__(self):
        return u"{ip} - {cty}".format(ip=self.ip, cty=self.city)


# deprecated, willed be removed some day
class AccessLog(models.Model):
    ip = models.ForeignKey(RemoteIP)
    accessed_at = models.DateTimeField(auto_now_add=True, verbose_name=u'访问时间')
    request_path = models.CharField(max_length=128, null=True, blank=True, verbose_name=u'访问路径')

    save_interval = datetime.timedelta(0, 300)

    def __unicode__(self):
        return self.ip

    class Meta():
        verbose_name = u'来访记录'
        verbose_name_plural = u'来访记录'
