# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_split_social_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name', 'slug')]),
        ),
    ]
