#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

from feeds.views import BraterView

from feeds.views import FeedCreateView, FeedListView, FeedDetailView, FeedUpdateView, FeedDeleteView, FeedRefreshView
from feeds.views import PostListView, PostDetailView, PostTrackableView
from feeds.views import CategoryListView, CategoryCreateView, CategoryDetailView, CategoryUpdateView
from feeds.views import TagListView, TagDetailView, TagCreateView

from feeds.rss import RssFeed

urlpatterns = patterns('',
    url(r'^brater/$', BraterView.as_view(), name="brater"),
)

urlpatterns += patterns('',
    url(r'^$', FeedListView.as_view(), name="feed-home"), 
    url(r'^page/(?P<page>\w+)/$', FeedListView.as_view(), name="feed-home-paginated"), 
    url(r'^add/$', FeedCreateView.as_view(), name="feed-add"), 
    url(r'^(?P<pk>\d+)/$', FeedDetailView.as_view(), name="feed-view"), 
    url(r'^(?P<pk>\d+)/update/$', FeedUpdateView.as_view(), name="feed-update"),
    url(r'^(?P<pk>\d+)/delete/$', FeedDeleteView.as_view(), name="feed-delete"), 
    url(r'^(?P<pk>\d+)/refresh/$', FeedRefreshView.as_view(), name="feed-refresh"), 
)

urlpatterns += patterns('',
    url(r'^p/$', PostListView.as_view(), name="post-view"), 
    url(r'^p/(?P<pk>\d+)/$', PostDetailView.as_view(), name="post-view"), 
)

urlpatterns += patterns('',
     url(r'^f/(?P<pk>\d+)/$', RssFeed(), name="rss"), 
     url(r'^t/(?P<pk>\d+)/$', PostTrackableView.as_view(), name="post-trackable-view"), 
)

urlpatterns += patterns('',
    url(r'^category/$', CategoryListView.as_view(), name="category-home"), 
    url(r'^category/page/(?P<page>\w+)/$', CategoryListView.as_view(), name="category-home-paginated"), 
    url(r'^category/add/$', CategoryCreateView.as_view(), name="category-add"), 
    url(r'^category/(?P<slug>\w+)/$', CategoryDetailView.as_view(), name="category-view"), 
    url(r'^category/(?P<slug>\w+)/update$', CategoryUpdateView.as_view(), name="category-update"), 
)

urlpatterns += patterns('',
    url(r'^tag/$', TagListView.as_view(), name="tag-home"), 
    url(r'^tag/page/(?P<page>\w+)/$', TagListView.as_view(), name="tag-home-paginated"), 
    url(r'^tag/add/$', TagCreateView.as_view(), name="tag-add"), 
    url(r'^tag/(?P<slug>\w+)/$', TagDetailView.as_view(), name="tag-view"), 
)


from django.views.generic import TemplateView

urlpatterns += patterns('',
    url(r'test/rss1/$', TemplateView.as_view(template_name="feeds/tests/rss1.html"), name="rss1"),
    url(r'test/rss2/$', TemplateView.as_view(template_name="feeds/tests/rss2.html"), name="rss2"),
)