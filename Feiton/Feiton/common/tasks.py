#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import re
import requests
import json
import logging
import time
from smtplib import SMTPException
from django.core.mail import send_mail
from django.conf import settings
from Feiton.celery import app
from Feiton.common.models import RemoteIP

IPLIB_API_URL = 'http://ip.taobao.com/service/getIpInfo.php'
ip_info = (u'country', u'area', u'region', u'city', u'ip', u'isp',)
MAX_RETRY = 5
logger = logging.getLogger(__name__)


# deprecated
def query_ip_info(ip):
    params = {'ip': ip}
    ip_data = {}
    for i in range(MAX_RETRY):
        r = requests.get(IPLIB_API_URL, params=params)
        # TODO: sometimes the response from the api is not pure json...
        # wtf...change api?
        cleaned_response = re.sub('<script.*$', '', r.text)
        response_json = json.loads(cleaned_response)
        if response_json.get(u'code') == 0:
            ip_data.update(
                {k: response_json['data'][k]
                    for k in ip_info if k in response_json['data']}
            )
            RemoteIP.objects.filter(ip=ip).update(**ip_data)
            break
        else:
            time.sleep(0.5 * i)
    return None


@app.task
def send_email(**kwargs):
    """
    the following arguments are required in kwargs:
        name,
        subject,
        content,
        email,
    """
    subject = settings.EMAIL_SUBJECT_PREFIX + '-' + kwargs['name'] + ':' + kwargs['subject']
    content = kwargs.get('email', '') + '\n' + kwargs['content']
    to_address = settings.EMAIL_ADDRESS_LIST
    for i in range(3):
        try:
            send_mail(
                subject,
                content,
                settings.EMAIL_HOST_USER,
                to_address,
                fail_silently=False)
            break
        except SMTPException as e:
            logger.error("send email failed, retrying..., reason:%s", e)
    return
