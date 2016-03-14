# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from Feiton.common.models import RemoteIP, AccessLog
from .tasks import query_ip_info


class AccessMiddleware(object):

    def process_request(self, request):
        ip = get_client_ip(request)
        ipinfo, created = RemoteIP.objects.get_or_create(ip=ip)
        if created:
            query_ip_info.delay(ip)
        if not request.path.startswith('/admin'):
            AccessLog.objects.create(ip=ipinfo, request_path=request.path)
        return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def record_ip(func):
    def wrapped_func(request, *args, **kwargs):
        ip = get_client_ip(request)
        ipinfo, created = RemoteIP.objects.get_or_create(ip=ip)
        # TODO: what if the task failed? Ensure that info is acquired.
        if created:
            query_ip_info.delay(ip)
        AccessLog.objects.create(ip=ipinfo, request_path=request.path)
        return func(request, *args, **kwargs)
    return wrapped_func
