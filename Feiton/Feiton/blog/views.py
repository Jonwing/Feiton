#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.shortcuts import (render_to_response, get_object_or_404,
                              Http404, redirect)
from django.template import RequestContext
from django.views.generic import FormView

from Feiton.blog.forms import ContactForm
from Feiton.blog.models import Article, Topset, Statistic
from Feiton.common.logging import record_ip


def index(request):
    specified_post = Topset.objects.first().topset

    return render_to_response(
        "index.html",
        {"article": specified_post},
        context_instance=RequestContext(request))


def articles_list(request):
    all_articles = Article.objects.order_by("-publish_time").all()
    paginator = Paginator(all_articles, settings.ARTICLES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render_to_response("articles.html", {"articles": articles})


@record_ip
def article_detail(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    statistic = Statistic.objects.update_or_create(
        article=article,
        defaults={
            "visits": (article.statistic and article.statistic.visits+1 or 1)}
        )[0]
    return render_to_response(
        "article_detail.html",
        {
            "article": article,
            "statistic": statistic
            },
        context_instance=RequestContext(request)
        )


def about(request):
    raise Http404


@record_ip
def like_article(request, article_id):
    article = get_object_or_404(Article, pk=int(article_id))
    print article
    if not request.session.get('like_%s' % article_id, None):
        article.statistic.likes += 1
        article.statistic.save()
        request.session['like_%s' % article_id] = 'liked'

    return redirect("article_detail", id=article.id, slug=article.slug)


def sort_articles_by_month():
    '''
    return a list of articles grouped by month
    [[article01, article02,...],[article21,article22,...],...]
    will be deprecated soon.
    '''
    publish_times = Article.objects.values_list('publish_time', flat=True)
    months = set(
        [datetime.datetime(x.year, x.month, 1) for x in publish_times])
    sortedArticles = [Article.objects.filter(
        publish_time__year=x.year,
        publish_time__month=x.month)
        for x in months]
    return sortedArticles


class ContactView(FormView):
    template_name = 'contact_me.html'
    success_template = 'thanks.html'
    form_class = ContactForm

    def form_valid(self, form):
        form.send_format_mail(form.cleaned_data)
        return render_to_response(self.success_template)

    # TODO: @record ip?
    def post(self, request, *args, **kwargs):
        return super(ContactView, self).post(request, *args, **kwargs)
