# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.safestring import mark_safe
from mdeditor.fields import MDTextField  # noqa
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class UserInfo(models.Model):
    """
    用户扩展信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userinfo')
    users_avatar = 'users_avatar'
    avatar = models.ImageField(null=True, blank=True, upload_to=f'{users_avatar}', verbose_name='用户头像')
    mobile = models.CharField(null=True, blank=True, default='', max_length=11, verbose_name='手机号')
    wechat = models.CharField(null=True, blank=True, default='', max_length=30, verbose_name='微信')
    qq = models.CharField(null=True, blank=True, default='', max_length=10, verbose_name='QQ')
    blog_address = models.CharField(null=True, blank=True, default='', max_length=255, verbose_name='博客地址')
    introduction = models.TextField(null=True, blank=True, default='', verbose_name='自我介绍')

    class Meta:
        verbose_name = '用户扩展信息'
        verbose_name_plural = 'userinfo'

    def __str__(self):
        return self.user.username


class Carousel(models.Model):
    """
    首页轮播图配置
    """
    link = models.CharField(null=True, blank=True, default='#', max_length=255, verbose_name='链接')
    carousel = models.ImageField(upload_to='carousel', verbose_name='轮播图')
    carousel_title = models.TextField(blank=True, null=True, max_length=50, verbose_name='轮播图左下标题')
    img_link_title = models.TextField(blank=True, null=True, max_length=255, verbose_name='图片标题')
    img_alt = models.TextField(blank=True, null=True, max_length=255, verbose_name='轮播图alt')

    class Meta:
        verbose_name = '首页轮播图配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.carousel_title


class Conf(models.Model):
    """
    网站配置信息
    """
    main_website = models.CharField(null=True, blank=True, max_length=50, verbose_name='主网站', default="xwboy.top")
    name = models.CharField(null=True, blank=True, max_length=8, verbose_name='关注我_名称', default="CL' WU")
    chinese_description = models.CharField(null=True, blank=True, max_length=30, verbose_name='关注我_中文描述',
                                           default='永不放弃坚持就是这么酷！要相信光')
    english_description = models.TextField(null=True, blank=True, max_length=100, verbose_name='关注我_英文描述',
                                           default='Never give up persistence is so cool！Believe in the light！！！')
    avatar_link = models.CharField(null=True, blank=True, max_length=255, verbose_name='关注我_头像超链接')
    website_author = models.CharField(null=True, blank=True, max_length=10, verbose_name='网站作者', default='xiaowu')
    website_author_link = models.CharField(null=True, blank=True, max_length=255, verbose_name='网站作者链接',
                                           default='https://www.xwboy.top')
    email = models.EmailField(null=True, blank=True, max_length=30, verbose_name='作者收件邮箱',
                              default='2186656812@qq.com')
    website_number = models.CharField(null=True, blank=True, max_length=100, verbose_name='备案号')
    git = models.CharField(null=True, blank=True, max_length=255, verbose_name='git链接',
                           default='https://gitee.com/wu_cl')
    website_logo = models.ImageField(null=True, blank=True, upload_to='logo', verbose_name='网站logo')

    @staticmethod
    def fetch_all_site_info():
        # 获取站点信息
        site_info = cache.get("site_info")
        if not site_info:
            # 查询最后一条站点信息
            site_info = Conf.objects.last()
            # 保存站点信息存到缓存redis中 缓存 60s*2
            if site_info:
                # 如果查询到了站点信息就缓存
                cache.set("site_info", site_info, 120)
        return site_info

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.main_website


class HeadAnnouncement(models.Model):
    """
    轮播公告
    """
    head_announcement = models.CharField(max_length=50, verbose_name='头部轮播公告', default='热烈欢迎浏览本站')

    class Meta:
        verbose_name = '轮播公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.head_announcement


class MainAnnouncement(models.Model):
    """
    主公告
    """
    main_announcement = models.TextField(verbose_name='右侧公告', default='📢')

    class Meta:
        verbose_name = '主公告'
        verbose_name_plural = verbose_name

    def ment_text(self):
        """
        后台字数显示控制
        """
        if len(str(self.main_announcement)) > 188:
            return f'{str(self.main_announcement)[0:188]}……'
        else:
            return str(self.main_announcement)

    def __str__(self):
        return self.main_announcement


class Friend(models.Model):
    """
    友链
    """
    url = models.CharField(max_length=255, verbose_name='友链链接', default='https://my.oschina.net/chulan')
    title = models.CharField(max_length=50, verbose_name='超链接title', default='OSCHINA')
    name = models.CharField(max_length=20, verbose_name='友链名称', default='chulan')

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.url


class Pay(models.Model):
    """
    收款图
    """
    pay_img = models.ImageField(blank=True, null=True, upload_to='pay', verbose_name='捐助收款图')

    class Meta:
        verbose_name = '捐助收款图'
        verbose_name_plural = verbose_name


class About(models.Model):
    """
    关于
    """
    contents = MDTextField(verbose_name='关于Text')

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = verbose_name

    def about_text(self):
        """
        后台字数显示控制
        """
        if len(str(self.contents)) > 200:
            return f'{str(self.contents)[0:200]}……'
        else:
            return str(self.contents)

    def __str__(self):
        return self.contents


class Tag(models.Model):
    """
    标签
    """
    tag_name = models.CharField('标签名称', max_length=30)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=100, verbose_name='文章标题')
    content = MDTextField(blank=True, null=True, verbose_name='文章正文')
    digest = models.TextField(blank=True, null=True, verbose_name='文章摘要')
    view = models.BigIntegerField(default=0, verbose_name='阅读数')
    comment = models.BigIntegerField(default=0, verbose_name='评论数')
    picture = models.CharField(max_length=255, blank=True, null=True, verbose_name="url(标题图链接)")
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='文章类型')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        ordering = ['-created_time']  # 按时间降序
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name

    def content_text(self):
        """
        后台正文字数显示控制
        """
        if len(str(self.content)) > 30:
            return f'{str(self.content)[0:30]}……'  # 超出部分以省略号代替。
        else:
            return str(self.content)

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])

    def commenced(self, num):
        """
        刷新评论数
        :return:
        """
        self.comment = num
        self.save(update_fields=['comment'])

    def __str__(self):
        return self.title


class ArticleImg(models.Model):
    """
    文章大头图
    """
    img_title = models.CharField(max_length=50, verbose_name='图片标题')
    article_img = models.ImageField(upload_to='article_img', verbose_name='文章大头图')

    def url(self):
        """
        显示图片url
        """
        if self.article_img:
            return self.article_img.url
        else:
            return "url为空"

    def images(self):
        """
        预览图
        """
        try:
            href = self.article_img.url
            img = mark_safe('<img src="%s" width="100px" />' % href)
        except Exception:  # noqa
            img = ''
        return img

    # 修改列名显示
    url.short_description = 'URL ( 复制粘贴即可 )'
    images.short_description = '图片预览'
    images.allow_tags = True

    def __str__(self):
        return self.img_title


class Category(models.Model):
    """
    文章类型
    """
    name = models.CharField('文章类型', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    @staticmethod
    def fetch_all_category():
        """
        获取所有的分类
        :return:
        """
        all_category = Category.objects.all()
        return all_category

    class Meta:
        ordering = ['name']
        verbose_name = "文章类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(MPTTModel):
    """
    评论
    """
    title = models.CharField("标题", max_length=100)
    name = models.CharField('昵称', max_length=25)
    request_ip = models.CharField('请求者ip', max_length=30, default='未知')
    request_address = models.CharField('请求者地址', max_length=100, default=None)
    email = models.EmailField('预留邮箱', null=True, blank=True, max_length=50)
    comment = models.TextField('评论内容', max_length=500)
    avatar_address = models.ImageField('头像', null=True, blank=True)
    url = models.CharField('链接', max_length=255)
    url_input = models.CharField('输入链接', null=True, blank=True, max_length=255)
    created_time = models.DateTimeField('评论时间', auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    reply = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='reply')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    class MPTTMeta:
        order_insertion_by = ['created_time']  # https://github.com/django-mptt/django-mptt/issues/167

    def comment_validity(self):
        """
        后台字数显示控制
        """
        if len(str(self.comment)) > 30:
            return f'{str(self.comment)[0:30]}……'
        else:
            return str(self.comment)

    def avatar_link(self):
        """
        头像预览图
        """
        try:
            href = self.avatar_address.url
            img = mark_safe(f'<img src="{href}" width="60px" height="60px" />')
        except Exception:  # noqa
            img = ''
        return img

    def __str__(self):
        return self.comment[:20]


class Subscription(models.Model):
    """
    文章邮箱订阅
    """
    email = models.EmailField('邮箱订阅用户', max_length=50)
    sub_time = models.DateTimeField('订阅时间', auto_now_add=True)

    class Meta:
        ordering = ['sub_time']
        verbose_name = '邮箱订阅'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email
