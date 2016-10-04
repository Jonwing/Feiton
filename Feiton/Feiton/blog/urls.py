#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from django.conf.urls import patterns, url
from .views import ArticlesView

urlpatterns = patterns(
    'Feiton.blog.views',
    url(r"^$", 'articles_list', name='articles'),
    url(r"^favorite/(?P<article_id>\w+)$", 'like_article', name='like_article'),
    url(r"^(?P<id>\w+)/(?P<slug>\S+)$", 'article_detail', name="article_detail"),
    url(r"^archieve$", ArticlesView.as_view(), name="archieve"),
)
