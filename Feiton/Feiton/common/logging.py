# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from Feiton.common.models import RemoteIP, AccessLog
from .tasks import query_ip_info


class AccessMiddleware(object):

    def process_request(self, request):
        ip = self.get_client_ip(request)
        # ip_data = self.query_ip_info(ip)
        ipinfo, created = RemoteIP.objects.get_or_create(ip=ip)
        if created:
            query_ip_info.delay(ip)
        if not request.path.startswith('/admin'):
            AccessLog.objects.create(ip=ipinfo, request_path=request.path)
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
