# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('forum', '0003_topic_date'), ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.CharField(
                default='test', max_length=1000),
            preserve_default=False, ),
    ]
