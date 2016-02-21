#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from celery import task

from common.models import RemoteIP

IPLIB_API_URL = 'http://ip.taobao.com/service/getIpInfo.php'
ip_info = (u'country', u'area', u'region', u'city', u'ip', u'isp',)


@task()
def query_ip_info(ip):
    params = {'ip': ip}
    ip_data = {}
    r = requests.get(IPLIB_API_URL, params=params)
    response_json = r.json()
    print "querying ip info..."
    if response_json.get(u'code') == 0:
        ip_data.update(
            {k: response_json['data'][k] for k in ip_info if k in response_json['data']}
            )
        RemoteIP.objects.filter(ip=ip).update(**ip_data)
    print "DOne"
    return None
