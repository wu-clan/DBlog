#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""""""""""""""""""""""" models监听器分割线 """""""""""""""""""""""""""""

# 创建用户时自动调用，绑定用户和用户信息
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from blog.models import Carousel, ArticleImg, Pay, Conf, UserInfo


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    同步创建对应用户扩展信息
    """
    if created:
        UserInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    """
    同步更新用户扩展信息
    """
    instance.userinfo.save()


@receiver(post_delete, sender=UserInfo)
def delete_user_avatar_files(sender, instance, **kwargs):
    """
    注销用户时同步删除头像文件
    """
    instance.avatar.delete(None)


@receiver(pre_delete, sender=Carousel)
def delete_carousel_files(sender, instance, **kwargs):
    """
    同步删除轮播图文件
    """
    instance.carousel.delete(False)


@receiver(pre_delete, sender=ArticleImg)
def delete_article_img_files(sender, instance, **kwargs):
    """
    同步删除文章大头图文件
    """
    instance.article_img.delete(False)


@receiver(pre_delete, sender=Pay)
def delete_payimg_files(sender, instance, **kwargs):
    """
    同步删除捐助图文件
    """
    instance.payimg.delete(False)


@receiver(pre_delete, sender=Conf)
def delete_website_logo_files(sender, instance, **kwargs):
    """
    同步删除网站logo文件
    """
    instance.website_logo.delete(False)
