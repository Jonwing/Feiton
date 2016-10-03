# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=64, verbose_name='\u6807\u9898')),
                ('subcaption', models.CharField(max_length=64, verbose_name='\u526f\u6807\u9898', blank=True)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('is_private', models.BooleanField(default=False)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('shorttext', models.CharField(max_length=256, verbose_name='\u77ed\u63cf\u8ff0', blank=True)),
                ('slug', models.SlugField(default='detail', max_length=128)),
            ],
            options={
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0\u4eec',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u4f5c\u8005\u59d3\u540d')),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': '\u4f5c\u8005',
                'verbose_name_plural': '\u4f5c\u8005',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u5206\u7c7b')),
                ('code', models.CharField(unique=True, max_length=32, verbose_name='code')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u7c7b\u522b',
                'verbose_name_plural': '\u7c7b\u522b',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(default=True)),
                ('reply_to', models.IntegerField(null=True)),
                ('commenter', models.CharField(max_length=30)),
                ('commenter_email', models.EmailField(max_length=254, blank=True)),
                ('content', models.TextField(blank=True)),
                ('article', models.ForeignKey(to='blog.Article')),
            ],
            options={
                'ordering': ['-created_time'],
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba\u4eec',
            },
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visits', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('article', models.OneToOneField(to='blog.Article')),
            ],
            options={
                'verbose_name': '\u7edf\u8ba1',
                'verbose_name_plural': '\u7edf\u8ba1',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='\u6807\u7b7e')),
                ('code', models.CharField(unique=True, max_length=32, verbose_name='code')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='Topset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('topset', models.ForeignKey(to='blog.Article')),
            ],
            options={
                'ordering': ['-created_time'],
                'verbose_name': '\u7f6e\u9876',
                'verbose_name_plural': '\u7f6e\u9876',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(to='blog.Author'),
        ),
        migrations.AddField(
            model_name='article',
            name='catagory',
            field=models.ForeignKey(to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
