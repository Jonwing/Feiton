#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea)
