#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from Feiton.common.tasks import send_email


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label=u'您的名字')
    email = forms.EmailField(label=u'Email')
    subject = forms.CharField(max_length=50, label=u'邮件主题')
    content = forms.CharField(widget=forms.Textarea, label=u'邮件内容')

    def send_format_mail(self, dictionary):
        send_email.delay(**dictionary)
