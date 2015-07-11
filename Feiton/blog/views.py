#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    Http404,
    redirect
    )
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
    DUOSHUO_COMMENTS_SYNC_URL,
    DUOSHUO_SECRET,
    DUOSHUO_LOCAL_DOMAIN_NAME
    )

from utils.mails import send_format_mail
from utils.duoshuoapi import get_comments_from_duoshuo


def index(request):
    specified_post = Topset.objects.order_by("-created_time").first().topset

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


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
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


def like_article(request, article_id, like=0):
    article = get_object_or_404(Article, id=article_id)
    print like
    if like:
        article.statistic.likes += 1
        article.statistic.save()

    return redirect("article_detail", article_id=article.id)


@csrf_exempt
def sync_comments(request):
    # TODO: validate signature
    print request.POST
    json_comment = get_comments_from_duoshuo(
        DUOSHUO_COMMENTS_SYNC_URL,
        short_name=DUOSHUO_LOCAL_DOMAIN_NAME,
        secret=DUOSHUO_SECRET
        )
    for cm in json_comment['response']:
        if cm['action'] == 'create':
            try:
                article = Article.objects.get(id=cm['meta']['thread_key'])
            except ObjectDoesNotExist:
                continue
            comment = Comment(
                article=Article.objects.get(id=cm['meta']['thread_key']),
                commenter=cm['meta'].get('author_name', 'Passanger'),
                commenter_email=cm['meta'].get('author_email', None),
                content=cm['meta'].get('message', 'no message'),
                created_time=cm['meta']['created_at']
                )
            comment.save()
