# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0007_move_category_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='Feed',
            name='logo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
