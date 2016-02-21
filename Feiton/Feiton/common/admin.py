from __future__ import unicode_literals
from django.contrib import admin
from .models import RemoteIP


class RemoteIPAdmin(admin.ModelAdmin):
    empty_value_display = u'----'
    fields_ = ('ip', 'country', 'region', 'city', 'isp', 'assessed_at', 'request_path',)
    list_filter = ('ip',)

admin.site.register(RemoteIP, RemoteIPAdmin)
