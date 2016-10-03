#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

env = os.environ.get

DEBUG = env('DEBUG', False)

STATIC = env('STATIC', '/data')
STATIC_ROOT = STATIC + '/statics'
MEDIA_ROOT = STATIC_ROOT + '/media'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('MYSQL_DATABASE'),
        'USER': env('MYSQL_USER',),
        'PASSWORD': env('MYSQL_PASSWORD'),
        'HOST': env('MYSQL_HOST'),
        'PORT': env('MYSQL_PORT', 3306)
    }
}

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN', '')
}

# Email settings
EMAIL_HOST = env('EMAIL_HOST', '')
EMAIL_PORT = env('EMAIL_PORT', '')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', '')
EMAIL_ADDRESS_LIST = [env('ENAIL_ADDRESS_LIST', '')]
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', '')

# duoshuo comments SDK settings
# DUOSHUO_SHORT_NAME = 'Feiton'
# DUOSHUO_LOCAL_DOMAIN_NAME = 'jonwing'
# DUOSHUO_BASE_URL = 'http://api.duoshuo.com'
# DUOSHUO_COMMENTS_SYNC_POSTFIX = '/log/list.json'
# DUOSHUO_COMMENTS_POSTFIX = '/threads/counts'

# redis settings
REDIS_HOST = env('REDISSERVER_HOST', '')
REDIS_PORT = env('REDISSERVER_PORT', '')
REDIS_ZONE = env('REDISSERVER_ZONE', '0')
BROKER_URL = ''.join(['redis://', REDIS_HOST, ':', REDIS_PORT, '/', REDIS_ZONE])

# celery
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
