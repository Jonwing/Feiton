#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import
import datetime

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import (render_to_response, get_object_or_404,
                              Http404, redirect)
from django.template import RequestContext
from django.views.generic import FormView, ListView

from Feiton.blog.forms import ContactForm
from Feiton.blog.models import Article, Topset, Statistic, Tag, Category


def render_with_common_context(template_name, dct=None, context_instance=None):
    '''
    get common context, tags, categories, etc...
    '''
    ctx = {
        'tags': Tag.objects.all(),
        'ctgs': Category.objects.all()
    }
    ctx.update(dct) if dct else ctx
    return render_to_response(template_name, ctx, context_instance)


def index(request):
    '''
    index page, a timeline
    '''
    # specified_post = Topset.objects.first().topset
    timeline = Article.objects.order_by('-update_time').all()

    return render_with_common_context(
        "index.html",
        {"objects": timeline},
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

    return render_with_common_context("articles.html", {"articles": articles})


def article_detail(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    statistic = Statistic.objects.update_or_create(
        article=article,
        defaults={"visits": (article.statistic and article.statistic.visits + 1 or 1)}
    )[0]
    return render_with_common_context(
        "article_detail.html",
        {
            "article": article,
            "statistic": statistic
        },
        context_instance=RequestContext(request)
    )


def about(request):
    raise Http404


def like_article(request, article_id):
    article = get_object_or_404(Article, pk=int(article_id))
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
        return render_with_common_context(self.success_template)

    def post(self, request, *args, **kwargs):
        return super(ContactView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'tags': Tag.objects.all(),
            'ctgs': Category.objects.all()
        })
        return super(ContactView, self).get_context_data(**kwargs)


class ArticlesView(ListView):
    '''
    A view used to render some articles of specific queries.
    Like filtered by tags or categories
    '''
    queryset = Article.objects.all()
    ordering = '-update_time'
    template_name = 'articles.html'
    context_object_name = 'articles'
    model = Article

    def get_articles(self, request):
        tag = request.GET.get('tag')
        ctg = request.GET.get('ctg')
        # if tag:
        #     return self.filter_by_tag(tag)
        # if ctg:
        #     return self.filter_by_category(ctg)
        self.filter_by_ctg_or_tag(ctg, tag)

    def filter_by_ctg_or_tag(self, ctg=None, tag=None):
        if not ctg and not tag:
            return
        # filter_model = Category if ctg else Tag
        filter_kwarg = {'catagory__code': ctg} if ctg else {'tags__code': tag}
        self.queryset = Article.objects.filter(**filter_kwarg)

    def archieve(self):
        pass

    def get(self, request, *args, **kwargs):
        self.get_articles(request)
        return super(ArticlesView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'tags': Tag.objects.all(),
            'ctgs': Category.objects.all()
        })
        return super(ArticlesView, self).get_context_data(**kwargs)
