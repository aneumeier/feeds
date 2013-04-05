#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
async tasks, run via celery

updated to work with celery3
"""

import logging
import types
import twitter
import httplib2
import simplejson
import feedparser

# from exceptions import ValidationError

from django.template.defaultfilters import slugify

from celery import task, Task
from celery.registry import tasks
from datetime import datetime, timedelta

from feeds import USER_AGENT
from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC

from feeds.tools import mtime
from feeds.models import Feed, Post, Tag, Category


def get_entry_guid(entry, feed_id=None):
    """
    Get an individual guid for an entry
    """
    guid = None
    if entry.get('id', ''):
        guid = entry.get('id', '')
    elif entry.link:
        guid = entry.link
    elif entry.title:
        guid = entry.title

    if feed_id and not guid:
        feed = Feed.objects.get(pk=feed_id)
        guid = feed.link

    return entry.get('id', guid)



@task
def dummy(x=10):
    """
    Dummy Task that sleeps for x seconds,
    where the default for x is 10
    it returns True
    """
    from time import sleep
    print(__name__)
    logger = logging.getLogger(__name__)
    logger.info("dummy: invoked")
    logger.debug("Started to sleep for %ss"%x)
    sleep(x)
    logger.debug("Woke up after sleeping for %ss"%x)
    return True

@task
def entry_update_twitter(entry_id):
    """
    count tweets
    
    this is the old implementation 
    it is deprecated
    """
    logger = logging.getLogger(__name__)
    logger.debug("start: counting tweets")
    entry = Post.objects.get(pk=entry_id)
    twitter_count = "http://urls.api.twitter.com/1/urls/count.json?url=%s"
    query = twitter_count % (entry.link)

    resp, content = self.http.request(query, "GET")

    if resp.has_key('status') and resp['status'] == "200":
        result = simplejson.loads(content)
    else:
        print resp, content

    entry.tweets = resp['count']
    entry.save()
    logger.debug("stop: counting tweets")
    return True

@task
def entry_tags(entry_id, tags):
    logger = logging.getLogger(__name__)
    logger.debug("start: entry tags: %s"%(tags))
    
    entry = Post.objects.get(pk=entry_id)

    if tags is not "":
        if isinstance(tags, types.ListType):
            for tag in tags:
                t, created = Tag.objects.get_or_create(name=str(tag.term), slug=slugify(tag.term))
                if created:
                    t.save()
                p.tags.add(t)
            p.save()
    logger.debug("stop: entry tags")
    return

@task
def entry_process(entry, feed_id, postdict, fpf):
    """
    Receive Entry, process

    entry has these keys: (Spiegel.de)
     - 'summary_detail'
     - 'published'
     - 'published_parsed'
     - 'links'
     - 'title'
     - 'tags'
     - 'summary'
     - 'content'
     - 'guidislink'
     - 'title_detail'
     - 'link'
     - 'id'
    """

    logger = logging.getLogger(__name__)
    logger.debug("start: entry")
    feed = Feed.objects.get(pk=feed_id)
    logger.debug("Keys in entry '%s': %s"%(entry.title, entry.keys()))
    p, created = Post.objects.get_or_create(
        feed=feed, 
        title=entry.title, 
        guid=get_entry_guid(entry, feed_id), 
        published=True
    )
    
    if created:
        logger.debug("'%s' is a new entry"%(entry.title))
        p.save()
    
    p.link = entry.link
    p.content = entry.content[0].value
    p.save()

    if entry.has_key('tags'):
        entry_tags.delay(p.id, entry.tags)

    logger.debug("stop: entry")
    return True

@task
def feed_refresh(feed_id, **kwargs):
    logger = logging.getLogger(__name__)
    feed = Feed.objects.get(pk=feed_id)
    logger.debug("start")
    logger.info("collecting new posts for feed: %s (ID: %s)"%(feed.name, feed.id))

    feed_stats = { 
        ENTRY_NEW:0,
        ENTRY_UPDATED:0,
        ENTRY_SAME:0,
        ENTRY_ERR:0
    }

    try:
        fpf = feedparser.parse(feed.feed_url, agent=USER_AGENT, etag=feed.etag)
    except Exception, e: # Feedparser Exeptions
        logger.error('Feedparser Error: (%s) cannot be parsed: %s'%(feed.feed_url, str(e)))
        
    if hasattr(fpf, 'status'):
        # feedparsere returned a status
        if fpf.status == 304:
            # this means feed has not changed
            logger.debug("%s (ID: %s) has not changed"%(feed.name, feed.id))
            return False
        if fpf.status >= 400:
            # this means a server error
            logger.debug("%s (ID: %s) gave a server error"%(feed.name, feed.id))
            return False
    if hasattr(fpf, 'bozo') and fpf.bozo:
        logger.debug('[%d] !BOZO! Feed is not well formed: %s' % (feed.id, feed.name))
        
    feed.etag = fpf.get('etag', '')

    # some times this is None (it never should) *sigh*
    if feed.etag is None:
        feed.etag = ''

    try:
        feed.last_modified = mtime(fpf.modified)
    except Exception, e:
        feed.last_modified = datetime.now()
        logger.debug('[%s] last_modified not well formed: %s Reason: %s' % (feed.name, feed.last_modified, str(e)))
        
    feed.title = fpf.feed.get('title', '')[0:254]
    feed.tagline = fpf.feed.get('tagline', '')
    feed.link = fpf.feed.get('link', '')
    feed.last_checked = datetime.now()

    guids = []
    for entry in fpf.entries:
            guid = get_entry_guid(entry)
            guids.append(guid)
    logger.debug("guids: %s"%(str(guids)))

    try:
        feed.save()
    except Feed.last_modified.ValidationError, e:
        logger.warning("Feed.ValidationError: %s"%str(e))


    if guids:
        """
        fetch posts that we have on file already
        """
        postdict = dict([(post.guid, post) for post in Post.objects.filter(feed=feed.id).filter(guid__in=guids)])
        logger.debug("postdict keys: %s"%(postdict.keys()))
    else:
        """
        we didn't find any guids. leave postdict empty
        """
        postdict = {}

    for entry in fpf.entries:
        try:
            # feed_id, options, entry, postdict, fpf
            logger.debug("spawning task: %s %s"%(entry.title, feed_id)) # options are optional
            entry_process.delay(entry, feed_id, postdict, fpf) #options are optional
        except Exception, e:
            logger.debug("could not spawn task: %s"%(str(e)))

    feed.save()
    logger.debug("stop")
    return True

@task
def aggregate(**kwargs):
    """
    aggregate feeds

    type: celery task

    find all tasks that are marked for beta access

    .. codeauthor: Andreas Neumeier
    """
    from celery import group
    logger = logging.getLogger(__name__)
    logger.debug("start aggregating")
    feeds = Feed.objects.filter(is_active=True).filter(beta=True)
    logger.debug("processing %s feeds"%(feeds.count()))
    job = group([feed_refresh.s(i.id) for i in feeds])
    job.apply_async()
    logger.debug("stop aggregating")
    return True
