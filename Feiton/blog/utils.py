#! /usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from HTMLParser import HTMLParser


# get HTML summary
class HTMLSummary(HTMLParser):

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
