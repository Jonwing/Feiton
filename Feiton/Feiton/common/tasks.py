#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import requests
import json
from smtplib import SMTPException
from django.core.mail import send_mail
from Feiton.celery import app
from Feiton.common.models import RemoteIP
from Feiton.settings import EMAIL_SUBJECT_PREFIX, EMAIL_ADDRESS_LIST

IPLIB_API_URL = 'http://ip.taobao.com/service/getIpInfo.php'
ip_info = (u'country', u'area', u'region', u'city', u'ip', u'isp',)


@app.task
def query_ip_info(ip):
    params = {'ip': ip}
    ip_data = {}
    r = requests.get(IPLIB_API_URL, params=params)
    # TODO: sometimes the response from the api is not pure json...
    # wtf...change api?
    cleaned_response = re.sub('<script.*$', '', r.text)
    response_json = json.loads(cleaned_response)
    if response_json.get(u'code') == 0:
        ip_data.update(
            {k: response_json['data'][k] for k in ip_info if k in response_json['data']}
            )
        RemoteIP.objects.filter(ip=ip).update(**ip_data)
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
    subject = EMAIL_SUBJECT_PREFIX + '-' + kwargs['name'] + ':' + kwargs['subject']
    content = kwargs.get('email', 'nomail@somewhere.com') + '\n' + kwargs['content']
    from_address = kwargs.get('email', 'noreply@feiton.com')
    to_address = EMAIL_ADDRESS_LIST
    for i in range(3):
        try:
            send_mail(
                subject,
                content,
                from_address,
                to_address,
                fail_silently=False)
            break
        except SMTPException:
            print "send email failed, retrying..."
    return
