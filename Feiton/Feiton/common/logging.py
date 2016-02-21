# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import requests
from Feiton.common.models import RemoteIP

IPLIB_API_URL = 'http://ip.taobao.com/service/getIpInfo.php'


class AccessMiddleware(object):
    ip_info = (u'country', u'area', u'region', u'city', u'ip', u'isp',)

    # logging the ip into db
    # TODO: store ip first, do the info query later using celery
    def process_request(self, request):
        ip = self.get_client_ip(request)
        ip_data = self.query_ip_info(ip)
        if ip_data and not request.path.startswith('/admin'):
            RemoteIP.objects.create(request_path=request.path, **ip_data)

        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def query_ip_info(self, ip):
        params = {'ip': ip}
        ip_data = {}
        r = requests.get(IPLIB_API_URL, params=params)
        response_json = r.json()
        if response_json.get(u'code') == 0:
            ip_data.update(
                {k: response_json['data'][k] for k in self.ip_info if k in response_json['data']}
                )
        return ip_data
