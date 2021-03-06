#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from mistune import markdown


class Author(models.Model):
    name = models.CharField(u"作者姓名", max_length=50)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    class Meta:
        verbose_name = u'作者'
        verbose_name_plural = u'作者'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(u"标签", max_length=30, unique=True)
    code = models.CharField(u'code', max_length=32, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(u"分类", max_length=50, unique=True)
    code = models.CharField(u'code', max_length=32, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'类别'
        verbose_name_plural = u'类别'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    caption = models.CharField(u"标题", max_length=64)
    subcaption = models.CharField(u"副标题", max_length=64, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    author = models.ForeignKey(Author)
    catagory = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    content = RichTextUploadingField()
    shorttext = models.CharField(u'短描述', max_length=256, blank=True)
    slug = models.SlugField(max_length=128, default=u'detail')
    is_md = models.BooleanField(verbose_name='is markdown format', default=False)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章们'

    def __unicode__(self):
        return self.caption

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content = markdown(self.content)
            self.is_md = False
        super(Article, self).save(*args, **kwargs)
        statistic, created = Statistic.objects.get_or_create(article=self)

    @property
    def newer(self):
        '''
        return the newer post
        '''
        return Article.objects.filter(publish_time__gt=self.publish_time).first() or self

    @property
    def older(self):
        '''
        return the older post
        '''
        return Article.objects.filter(publish_time__lt=self.publish_time).last() or self

    def get_absolute_url(self):
        return reverse('article_detail', args=(self.id, self.slug))


class Statistic(models.Model):
    article = models.OneToOneField(Article)
    visits = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'统计'
        verbose_name_plural = u'统计'

    def __unicode__(self):
        return u"statistic of %s" % self.article


class Topset(models.Model):
    topset = models.ForeignKey(Article)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'置顶'
        verbose_name_plural = u'置顶'
        ordering = ['-created_time']

    def __unicode__(self):
        return self.topset.caption


class Comment(models.Model):
    article = models.ForeignKey(Article)
    created_time = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    reply_to = models.IntegerField(null=True)
    commenter = models.CharField(max_length=30)
    commenter_email = models.EmailField(blank=True)
    content = models.TextField(blank=True)

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = u'评论们'
        ordering = ['-created_time']

    def __unicode__(self):
        return str(self.commenter) + "'s comment on " + str(self.article)


# signal registration
# deprecated, not used any more
# @receiver(post_save, sender=Comment)
# def new_comment_remind(sender, **kwargs):
#     new_comment = kwargs.get('instance', None)
#     if new_comment:
#         mail = {
#             'name': new_comment.commenter + "'s comment on ",
#             'subject': str(new_comment.article),
#             'email': new_comment.commenter_email
#             if new_comment.commenter_email else 'someone@unknow.com',
#             'content': new_comment.content
#         }
#         send_format_mail(mail)
#     else:
#         return
