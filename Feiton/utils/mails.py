#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from Feiton.settings import EMAIL_SUBJECT_PREFIX, EMAIL_ADDRESS_LIST


def send_format_mail(dictionary):
    """
    the argument dictionary is like{
        'name': xxx,
        'subject': xxx,
        'email': xxx,
        'content': xxx
    }
    """
    subject = EMAIL_SUBJECT_PREFIX + '-' + dictionary['name'] + ':'\
        + dictionary['subject']
    content = dictionary.get('email', 'nomail@somewhere.com') + '\n' + dictionary['content']
    from_address = dictionary.get('email', 'nomail@somewhere.com')
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
