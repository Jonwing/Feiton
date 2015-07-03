#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    Http404,
    redirect)
from django.template import RequestContext
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
    )
from models import Article, Topset
from forms import ContactForm

from utils.mails import send_format_mail


# Create your views here.
def index(request):
    # TODO: get the top-post and place it on home page
    specified_post = Topset.objects.order_by("-create_time").first().article

    return render_to_response("index.html", {"article": specified_post})


def articles_list(request):
    all_articles = Article.objects.order_by("-publish_time").all()
    paginator = Paginator(all_articles, 15)
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
    return render_to_response("article_detail.html", {"article": article})


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
            mail_thread.join()

        return render_to_response("thanks.html")

    return render_to_response(
        "contact_me.html",
        context_instance=RequestContext(request)
        )


def about(request):
    raise Http404
