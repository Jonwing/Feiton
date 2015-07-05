#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from Feiton.settings import EMAIL_SUBJECT_PREFIX, EMAIL_ADDRESS_LIST


def send_format_mail(dictionary):
    subject = EMAIL_SUBJECT_PREFIX + '-' + dictionary['name'] + ':'\
        + dictionary['subject']
    content = dictionary['email'] + '\n' + dictionary['content']
    from_address = dictionary['email']
    to_address = EMAIL_ADDRESS_LIST
    try:
        send_mail(
            subject,
            content,
            from_address,
            to_address,
            fail_silently=False)
    except:
        return False
    return True
