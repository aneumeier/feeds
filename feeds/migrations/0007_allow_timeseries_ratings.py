# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 16:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_ratings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='updated_social',
        ),
        migrations.AddField(
            model_name='rating',
            name='id',
            field=models.AutoField(auto_created=True, default=django.utils.datetime_safe.datetime.now, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rating',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='feeds.Post'),
        ),
    ]
