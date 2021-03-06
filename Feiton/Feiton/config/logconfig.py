#!/usr/bin/env python
# -*- coding: utf-8 -*-

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'normal': {
            'format': '[%(levelname)1.1s %(asctime)s %(name)s|%(funcName)s|%(lineno)d]  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'normal'
        },
        'filelog': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/feiton_blg.log',
            'formatter': 'normal'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['filelog'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['filelog'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['filelog'],
            'propagate': False,
        },
        'Feiton': {
            'level': 'INFO',
            'handlers': ['filelog', 'sentry'],
        }
    },
}
