#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'blog.views',
    url(r'^home$', 'index', name='home_page'),
    )
