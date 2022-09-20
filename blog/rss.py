# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed

from .models import Article


class DBlogRssFeed(Feed):
    """ rss 订阅 , 仅显示文章摘要"""
    feed_type = Rss201rev2Feed
    title = 'xiaowu‘s django_blog'
    description = 'xiaowu的博客文章订阅'
    link = '/'

    # rss显示内容
    def items(self):
        return Article.objects.all()

    # 订阅标题
    def item_title(self, item):
        return item.title

    # 订阅摘要
    def item_description(self, item):
        return item.digest

    # 订阅链接
    def item_link(self, item):
        return reverse('blog:detail', args=(item.pk,))


class DBlogAtomFeed(DBlogRssFeed):
    """ Atom 子类"""
    feed_type = Atom1Feed  # 修改类型为 Atom1Feed
    subtitle = DBlogRssFeed.description
