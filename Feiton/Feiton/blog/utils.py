#! /usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import importlib
from HTMLParser import HTMLParser
from django.conf import settings
from django.conf.urls import url

url_patterns = importlib.import_module(settings.ROOT_URLCONF).urlpatterns


def register_path(path='', name=None):
    '''
    一个类似于flask @route('/xxx')的装饰器，写来玩玩～
    '''
    def func_wrapper(func):
        url_patterns.append(url(path, func, name=name))
        return func
    return func_wrapper


class HTMLSummary(HTMLParser):
    '''
    HTML摘要。
    '''

    def __init__(self, count):
        HTMLParser.__init__(self)
        self.count = count
        self.summary = u''

    def feed(self, text):
        assert(isinstance(text, unicode))
        HTMLParser.feed(self, text)

    def handle_data(self, data):
        more = self.count - len(self.summary)
        if more > 0:
            data_without_whitespace = u''.join(data.split())
            self.summary += data_without_whitespace[0:more]

    def get_summary(self, suffix=u'...', wrapper=u'p'):
        return u'<{0}>{1}{2}</{0}>'.format(wrapper, self.summary, suffix)
