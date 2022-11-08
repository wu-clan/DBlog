#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

from django import template
from django.utils import timezone

from blog.models import CommentExtend, ArticleExtend

register = template.Library()


@register.filter(name='article_praise_num')
def article_praise_num(article_id):
    """
    文章点赞数
    """
    ae = ArticleExtend.objects.filter(article_id=article_id)
    return ae.filter(praise=1).count() if ae else 0


@register.filter(name='comment_praise_num')
def comment_praise_num(comment_id):
    """
    评论点赞数
    """
    ce = CommentExtend.objects.filter(comment_id=comment_id)
    return ce.filter(praise=1).count() if ce else 0


@register.filter(name='comment_tread_num')
def comment_tread_num(comment_id):
    """
    评论踩数
    """
    te = CommentExtend.objects.filter(comment_id=comment_id)
    return te.filter(tread=1).count() if te else 0


@register.filter(name='is_user_praise')
def is_user_praise(comment_id, user):
    """
    用户是否赞
    """
    ce = CommentExtend.objects.filter(comment_id=comment_id).filter(user_id=user)
    return ce.first().praise if ce else False


@register.filter(name='is_user_tread')
def is_user_tread(comment_id, user):
    """
    用户是否踩
    """
    te = CommentExtend.objects.filter(comment_id=comment_id).filter(user_id=user)
    return te.first().tread if te else False


@register.filter(name='timesince_zh')
def timesince_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and 0 <= diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and 60 <= diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and 3600 <= diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if 1 <= diff.days < 30:
        return str(diff.days) + "天前"

    if 30 <= diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"
