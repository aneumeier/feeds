#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
      possible values for changefreq:
        'always'
        'hourly'
        'daily'
        'weekly'
        'monthly'
        'yearly'
        'never'
"""

from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models import Max

from feeds.models import Feed, Post, Category, Tag

class FeedSitemap(Sitemap):
    """
    SiteMap for Feeds
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Feed.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.last_modified

class PostSitemap(Sitemap):
    """
    SiteMap for Posts
      possible values for changefreq:
        'always'
        'hourly'
        'daily'
        'weekly'
        'monthly'
        'yearly'
        'never'
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        maximum = float(Post.objects.all().aggregate(Max('score'))['score__max'])
        if maximum > 0:
            priority = float(obj.score)/float(maximum)
        else:
            priority = 0

        if priority <= 0.1:
            priority = 0

        return priority

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.last_modified

class CategorySitemap(Sitemap):
    """
    SiteMap for Categories
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return datetime.now()

class TagSitemap(Sitemap):
    """
    SiteMap for Tags
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return datetime.now()