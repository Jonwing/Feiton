#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import datetime

from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    Http404,
    redirect
    )
from django.http import HttpResponse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
    )
from models import Article, Topset, Statistic, Comment
from forms import ContactForm
from Feiton.settings import (
    ARTICLES_PER_PAGE,
    DUOSHUO_BASE_URL,
    DUOSHUO_COMMENTS_SYNC_POSTFIX,
    DUOSHUO_COMMENTS_POSTFIX,
    DUOSHUO_SECRET,
    DUOSHUO_LOCAL_DOMAIN_NAME
    )

from utils.mails import send_format_mail
from utils.models import Duoshuoattr
from utils.duoshuoapi import get_comments_from_duoshuo


def index(request):
    specified_post = Topset.objects.first().topset

    return render_to_response("index.html", {"article": specified_post})


def articles_list(request):
    all_articles = Article.objects.order_by("-publish_time").all()
    paginator = Paginator(all_articles, ARTICLES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render_to_response("articles.html", {"articles": articles})


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
            }
        )


def contact_me(request):
    if request.method == 'POST':
        print request.POST
        letter = ContactForm(request.POST)
        if letter.is_valid():
            letter_cd = letter.cleaned_data
            mail_thread = threading.Thread(
                target=send_format_mail,
                name="Email thread",
                args=(letter_cd,)
                )
            mail_thread.start()
            # mail_thread.join()

        return render_to_response("thanks.html")

    return render_to_response(
        "contact_me.html",
        context_instance=RequestContext(request)
        )


def about(request):
    raise Http404


def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if not request.session.get('like_%s' % article_id, None):
        article.statistic.likes += 1
        article.statistic.save()
        request.session['like_%s' % article_id] = 'liked'

    return redirect("article_detail", article_id=article.id)


@csrf_exempt
def sync_comments(request):
    # TODO: validate signature
    # print request.POST
    last_log = Duoshuoattr.objects.order_by('-create_time')[0]
    json_comment = get_comments_from_duoshuo(
        DUOSHUO_BASE_URL+DUOSHUO_COMMENTS_SYNC_POSTFIX,
        short_name=DUOSHUO_LOCAL_DOMAIN_NAME,
        secret=DUOSHUO_SECRET,
        since_id=last_log.since_id
        )
    if json_comment is None:
        raise Http404
    for cm in json_comment['response']:
        if cm['action'] == 'create':
            try:
                article = Article.objects.get(id=cm['meta']['thread_key'])
            except ObjectDoesNotExist:
                continue
            comment, created = Comment.objects.update_or_create(
                article=Article.objects.get(id=cm['meta']['thread_key']),
                commenter=cm['meta'].get('author_name', 'Passanger'),
                commenter_email=cm['meta'].get('author_email', None),
                content=cm['meta'].get('message', 'no message'),
                defaults={'created_time': cm['meta']['created_at']}
                )
        if cm == json_comment['response'][-1]:
            last_sync_id = Duoshuoattr(since_id=int(cm['log_id']))
            last_sync_id.save()
    # update comment number
    all_articles = Article.objects.all()
    for article in all_articles:
        cms = Comment.objects.filter(article=article).count()
        if cms:
            Statistic.objects.update_or_create(
                article=article,
                defaults={'comments': article.statistic and cms or 0}
                )
    return HttpResponse(status=200)


def sort_articles_by_month():
    '''
    return a list of articles grouped by month
    [[article01, article02,...],[article21,article22,...],...]
    '''
    publish_times = Article.objects.values_list('publish_time', flat=True)
    months = set(
        [datetime.datetime(x.year, x.month, 1) for x in publish_times])
    sortedArticles = [Article.objects.filter(
        publish_time__year=x.year,
        publish_time__month=x.month)
        for x in months]
    return sortedArticles
