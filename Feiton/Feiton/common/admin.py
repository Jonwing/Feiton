from __future__ import unicode_literals
from django.contrib import admin
from .models import RemoteIP, AccessLog


class RemoteIPAdmin(admin.ModelAdmin):
    empty_value_display = u'----'
    list_display = ('ip', 'country', 'region', 'city', 'isp',)
    list_filter = ('ip',)

admin.site.register(RemoteIP, RemoteIPAdmin)


class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('ip', 'request_path', 'accessed_at')
    list_filter = ('ip', 'request_path',)

admin.site.register(AccessLog, AccessLogAdmin)
