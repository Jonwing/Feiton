#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'blog.views',
    url(r"^$", 'articles_list', name='articles'),
    url(r"^synccmts$", 'sync_comments', name="sync_comments"),
    url(r"^(?P<id>\w+)/(?P<slug>\S+)$", 'article_detail', name="article_detail"),
    url(r"^(?P<article_id>\w+)/like$", 'like_article', name='like_article'),
    )
