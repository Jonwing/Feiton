#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from DjangoUeditor.models import UEditorField


class Author(models.Model):
    name = models.CharField(u"作者姓名", max_length=50)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(u"标签", max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(u"分类", max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    caption = models.CharField(u"标题", max_length=30)
    subcaption = models.CharField(u"副标题", max_length=30, blank=True)
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author)
    catagory = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    content = UEditorField(
        verbose_name="content",
        imagePath=settings.UEDITOR_SETTINGS["upload"]["imagePathFormat"],
        filePath=settings.UEDITOR_SETTINGS["upload"]["filePathFormat"],
        settings=settings.UEDITOR_SETTINGS["config"],
        )
    abstract = models.TextField(blank=True)

    def __unicode__(self):
        return self.caption


class Statistic(models.Model):
    article = models.OneToOneField(Article)
    visits = models.IntegerField()
    comments = models.IntegerField()
    likes = models.IntegerField()

    def __unicode__(self):
        return u"blog statistics"
