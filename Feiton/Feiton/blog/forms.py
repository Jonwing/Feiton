#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.core.mail import send_mail
from Feiton.settings import EMAIL_SUBJECT_PREFIX, EMAIL_ADDRESS_LIST


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label=u'您的名字')
    email = forms.EmailField(label=u'Email')
    subject = forms.CharField(max_length=50, label=u'邮件主题')
    content = forms.CharField(widget=forms.Textarea, label=u'邮件内容')

    def send_format_mail(self, dictionary):
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
