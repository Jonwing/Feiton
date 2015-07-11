#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_comments_from_duoshuo(base_url, **kwargs):
    args = []
    for key, value in kwargs.items():
        args.append("%s=%s" % (key, value))
    query_args = '&'.join(args)
    query_url = '?'.join([base_url, query_args])
    response = urllib2.urlopen(query_url).read()
    json_data = json.loads(response)
    if json_data['code']:
        return None
    return json_data
