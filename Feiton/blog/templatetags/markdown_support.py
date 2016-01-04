#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from blog.models import Article

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown_support(content):
    return mark_safe(
        markdown2.markdown(
            force_text(content),
            extras=['fenced-code-blocks', 'cuddled-lists', 'metadata', 'tables', 'spoiler']))


@register.filter(name="urlize")
def get_id_and_slug(id):
    try:
        article = Article.objects.get(pk=id)
        return reverse('article_detail', args=[article.id, article.slug])
    except Article.DoesNotExist:
        return '#'
