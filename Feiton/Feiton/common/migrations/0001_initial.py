# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessed_at', models.DateTimeField(auto_now_add=True, verbose_name='\u8bbf\u95ee\u65f6\u95f4')),
                ('request_path', models.CharField(max_length=128, null=True, verbose_name='\u8bbf\u95ee\u8def\u5f84', blank=True)),
            ],
            options={
                'verbose_name': '\u6765\u8bbf\u8bb0\u5f55',
                'verbose_name_plural': '\u6765\u8bbf\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='RemoteIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(unique=True, max_length=64)),
                ('country', models.CharField(max_length=64, null=True, verbose_name='\u56fd\u5bb6', blank=True)),
                ('area', models.CharField(max_length=64, null=True, verbose_name='\u533a\u57df', blank=True)),
                ('region', models.CharField(max_length=64, null=True, verbose_name='\u7701\u4efd', blank=True)),
                ('city', models.CharField(max_length=64, null=True, verbose_name='\u57ce\u5e02', blank=True)),
                ('isp', models.CharField(max_length=32, null=True, verbose_name='\u8fd0\u8425\u5546', blank=True)),
            ],
            options={
                'ordering': ['-pk'],
                'verbose_name': 'ip\u4fe1\u606f',
                'verbose_name_plural': 'ip\u4fe1\u606f',
            },
        ),
        migrations.AddField(
            model_name='accesslog',
            name='ip',
            field=models.ForeignKey(to='common.RemoteIP'),
        ),
    ]
