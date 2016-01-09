#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
from blog.models import Article
from blog.utils import HTMLSummary

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


@register.filter(name="abstract")
def get_article_abstraction(content):
    summary_parser = HTMLSummary(settings.ABSTRACTION_LENGTH)
    summary_parser.feed(content)
    return summary_parser.get_summary()
