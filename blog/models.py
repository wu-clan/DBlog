# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

# 用户
# class User(AbstractUser):
#     u_name = models.CharField(max_length=20, verbose_name='昵称', default='')
#     birthday = models.DateField(verbose_name='生日', null=True, blank=True)
#     genter = models.CharField(max_length=2, choices=(("male", '男'), ('female', '女')), default='male')
#     image = models.ImageField(default='images/login/', max_length=200, null=True)
#     describe = models.CharField(max_length=500, default='', verbose_name='个性签名')
#
#     class Meta:
#         verbose_name = '用户信息'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.username
#
# # 邮箱验证码
# class EmailVerificationCode(models.Model):
#     code = models.CharField(max_length=20, verbose_name=u'验证码')
#     email = models.EmailField(max_length=200, verbose_name=u'邮箱')
#     send_type = models.CharField(max_length=10, choices=(("register", u'注册'), ("forget", u'密码找回')))
#     send_time = models.DateTimeField(auto_now_add=True, )
#
#     class Meta:
#         verbose_name = u'邮箱验证码'
#         verbose_name_plural = verbose_name


class Conf(models.Model):
    """
    配置信息
    """
    home_title = models.CharField(max_length=64, verbose_name='主页站点', default="Xwboy.top")
    carousel_announcement = models.CharField(max_length=30, verbose_name='头部轮播公告', default='热烈欢迎浏览本站')
    title = models.CharField(max_length=8, verbose_name='关注我_标题', default='热烈欢迎浏览本站')
    chinese_description = models.CharField(max_length=30, verbose_name='关注我_中文描述',
                                           default='永不放弃坚持就是这么酷！要相信光')
    english_description = models.CharField(max_length=100, verbose_name='关注我_英文描述',
                                           default='Never give up persistence is so cool！Believe in the light！！！')
    avatar_hyperlink = models.CharField(max_length=200, verbose_name='关注我_头像超链接',
                                           default='https://avatars.githubusercontent.com/u/52145145?v=4')
    website_designer = models.CharField(max_length=20, verbose_name='网站作者/about名称', default='xiaowu')
    design_author_hyperlink = models.CharField(max_length=200, verbose_name='设计作者超链接', default='http://www.xwboy.top')
    receiving_email_address = models.CharField(max_length=50, verbose_name='收件邮箱地址', default='2186656812@qq.com')
    record_number = models.CharField(max_length=100, verbose_name='备案号', default='豫ICP备 2021019092号-1')

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.home_title


class Pay(models.Model):
    """
    收款图
    """
    payvximg = models.ImageField(blank=True, null=True, verbose_name='微信捐助收款图')
    payaliimg = models.ImageField(verbose_name="支付宝捐助收款图")

    class Meta:
        verbose_name = '捐助收款图'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    标签
    """
    tag_name = models.CharField('标签名称', max_length=30, )

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=200, verbose_name='文章标题')  # 博客标题
    category = models.ForeignKey('Category',  verbose_name='文章类型', on_delete=models.CASCADE)
    date_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    content = models.TextField(blank=True, null=True, verbose_name='文章正文')
    digest = models.TextField(blank=True, null=True, verbose_name='文章摘要')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    view = models.BigIntegerField(default=0, verbose_name='阅读数')
    comment = models.BigIntegerField(default=0, verbose_name='评论数')
    picture = models.ImageField(verbose_name='url(标题图)')  # 标题图片地址
    tag = models.ManyToManyField(Tag)  # 标签

    class Meta:
        ordering = ['-date_time']  # 按时间降序
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name

    def sourceUrl(self):
        source_url = settings.HOST + '/blog/detail/{id}'.format(id=self.pk)
        return source_url  # 给网易云跟帖使用

    def content_validity(self):
        """
        狗太正文字数显示控制
        """
        if len(str(self.content)) > 20:  # 字数自己设置
            return '{}……'.format(str(self.content)[0:20])  # 超出部分以省略号代替。
        else:
            return str(self.content)

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])

    def commenced(self):
        """
        增加评论数
        :return:
        """
        self.comment += 1
        self.save(update_fields=['comment'])

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    文章类型
    """
    name = models.CharField('文章类型', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "文章类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    评论
    """
    title = models.CharField("标题", max_length=100)
    source_id = models.CharField('文章id或source名称', max_length=25)
    create_time = models.DateTimeField('评论时间', auto_now=True)
    user_name = models.CharField('评论用户', max_length=25)
    url = models.CharField('链接', max_length=100)
    comment = models.CharField('评论内容', max_length=500)

    class Meta:
        ordering = ['create_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
