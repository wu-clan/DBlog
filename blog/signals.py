#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from blog.models import Carousel, ArticleImg, Pay, Conf, UserInfo, Article, Subscription
from djangoProject import settings


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
def delete_pay_img_files(sender, instance, **kwargs):
    """
    同步删除捐助图文件
    """
    instance.pay_img.delete(False)


@receiver(pre_delete, sender=Conf)
def delete_website_logo_files(sender, instance, **kwargs):
    """
    同步删除网站logo文件
    """
    instance.website_logo.delete(False)


@receiver(post_save, sender=Article)
def send_stu_email(sender, created, **kwargs):
    """
    文章发布监听器，发布文章时触发并直接发送邮件订阅通知
    """
    if created:
        blog = Article.objects.filter()
        if blog:
            link_id = Article.objects.all().order_by('-id').first().pk
            title = blog.values('title').first().get('title').strip()
            # 文章链接
            # 本地调试时请将 settings.website_author_link 换成 http://127.0.0.1:端口号
            link = settings.website_author_link + f'/blog/detail/{link_id}'
            _email = Subscription.objects.filter().values_list('email', flat=True)
            if _email:
                email_list = _email[:99999999]
                email_title = "文章订阅推送"
                email_body = f"你订阅的 %s: %s 的博客发布新文章啦，快点击链接查阅吧\n文章：%s\n链接：%s" \
                             % (settings.website_author, settings.website_author_link, title, link)
                send_mail(
                    subject=email_title,
                    message=email_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=email_list,
                    auth_user=settings.EMAIL_HOST_USER,
                    auth_password=settings.EMAIL_HOST_PASSWORD,
                    fail_silently=True  # 如果你想确保订阅必须发送，请使用 False
                )
