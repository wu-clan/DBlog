# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.core.cache import cache  # 使用redis缓存
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.http import request
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from mdeditor.fields import MDTextField


# Create your models here.


class SiteUser(models.Model):
	"""
	网站用户
	"""

	username = models.CharField('账号', max_length=200, unique=True)
	password = models.CharField('密码', max_length=200)
	email = models.EmailField('邮箱', unique=True)
	time_joined = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

	class Meta:
		ordering = ['time_joined']
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name


class UserInfo(models.Model):
	"""
	用户扩展信息
	"""
	username = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='users_avatar', null=True, blank=True, verbose_name='用户头像')
	# 手机号格式正则校验
	mobile_validator = RegexValidator(r"^1[3-9]\d{9}$", "手机号码格式不正确")
	mobile = models.IntegerField(null=True, blank=True, verbose_name='手机号', validators=[mobile_validator])
	# sex_choice = (
	# 	(0, '女性'),
	# 	(1, '男性'),
	# )
	# sex = models.IntegerField(choices=sex_choice, default=1)
	wechart = models.CharField(null=True, blank=True, default='', max_length=50, verbose_name='微信')
	qq = models.CharField(null=True, blank=True, default='', max_length=10, verbose_name='QQ')
	blog_address = models.CharField(null=True, blank=True, default='', max_length=100, verbose_name='博客地址')
	introduction = models.TextField(null=True, blank=True, default='', max_length=500, verbose_name='自我介绍')

	class Meta:
		verbose_name = '用户扩展信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return ''


class Carousel(models.Model):
	"""
	首页轮播图配置
	"""
	carousel = models.ImageField(upload_to='carousel', verbose_name='轮播图')
	carousel_title = models.TextField(blank=True, null=True, max_length=100, verbose_name='轮播图左下标题')
	img_link_title = models.TextField(blank=True, null=True, max_length=100, verbose_name='图片标题')
	img_alt = models.TextField(blank=True, null=True, max_length=100, verbose_name='轮播图alt')

	class Meta:
		verbose_name = '首页轮播图配置'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.carousel_title


class Conf(models.Model):
	"""
	网站配置信息
	"""
	main_website = models.CharField(max_length=64, verbose_name='主网站', default="xwboy.top")
	name = models.CharField(max_length=8, verbose_name='关注我_名称', default="CL' WU")
	chinese_description = models.CharField(max_length=30, verbose_name='关注我_中文描述', default='永不放弃坚持就是这么酷！要相信光')
	english_description = models.TextField(max_length=100, verbose_name='关注我_英文描述',
	                                       default='Never give up persistence is so cool！Believe in the light！！！')
	avatar_link = models.CharField(max_length=150, verbose_name='关注我_头像超链接')
	website_author = models.CharField(max_length=20, verbose_name='网站作者', default='xiaowu')
	website_author_link = models.CharField(max_length=200, verbose_name='网站作者链接', default='http://www.xwboy.top')
	email = models.EmailField(max_length=50, verbose_name='作者收件邮箱', default='2186656812@qq.com')
	website_number = models.CharField(max_length=100, verbose_name='备案号', default='豫ICP备 2021019092号-1')
	git = models.CharField(max_length=100, verbose_name='git链接', default='https://gitee.com/wu_cl')
	website_logo = models.ImageField(upload_to='logo', verbose_name='网站logo', default='')

	@staticmethod
	def fetch_all_site_info():
		# 获取站点信息
		site_info = cache.get(f"site_info")
		if not site_info:
			# 查询最后一条站点信息
			site_info = Conf.objects.last()
			# 保存站点信息存到缓存redis中 缓存60*2
			if site_info:
				# 如果查询到了站点信息就缓存
				cache.set("site_info", site_info, 120)
		return site_info

	class Meta:
		verbose_name = '网站配置'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.main_website


class Announcement(models.Model):
	"""
	公告
	"""
	head_announcement = models.CharField(max_length=30, verbose_name='头部轮播公告', default='热烈欢迎浏览本站')
	main_announcement = models.TextField(blank=True, null=True, max_length=300, verbose_name='右侧公告',
	                                     default='暂无公告......')

	class Meta:
		verbose_name = '公告'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.head_announcement


class Friend(models.Model):
	"""
	友链
	"""
	url = models.CharField(max_length=200, verbose_name='友链链接', default='https://my.oschina.net/chulan')
	title = models.CharField(max_length=100, verbose_name='超链接title', default='OSCHINA')
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
	payimg = models.ImageField(upload_to='pay', blank=True, null=True, verbose_name='捐助收款图')

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

	def __str__(self):
		return self.contents


class Tag(models.Model):
	"""
	标签
	"""
	tag_name = models.CharField('标签名称', max_length=30, )

	class Meta:
		verbose_name = '标签'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.tag_name


class Article(models.Model):
	"""
	文章
	"""
	title = models.CharField(max_length=200, verbose_name='文章标题')  # 博客标题
	category = models.ForeignKey('Category', verbose_name='文章类型', on_delete=models.CASCADE)
	date_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
	content = MDTextField(blank=True, null=True, verbose_name='文章正文')
	digest = models.TextField(blank=True, null=True, verbose_name='文章摘要')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
	view = models.BigIntegerField(default=0, verbose_name='阅读数')
	comment = models.BigIntegerField(default=0, verbose_name='评论数')
	picture = models.CharField(max_length=300, blank=True, null=True, verbose_name="url(标题图链接)")
	tag = models.ManyToManyField(Tag)  # 标签

	class Meta:
		ordering = ['-date_time']  # 按时间降序
		verbose_name = '博客文章'
		verbose_name_plural = verbose_name

	def source_link(self):
		"""
		文章链接拼接
		"""
		source_url = settings.HOST + '/blog/detail/{id}'.format(id=self.pk)
		return source_url

	def content_validity(self):
		"""
		后台正文字数显示控制
		"""
		if len(str(self.content)) > 40:  # 字数自己设置
			return '{}……'.format(str(self.content)[0:40])  # 超出部分以省略号代替。
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
		href = self.article_img.url
		try:
			img = mark_safe('<img src="%s" width="100px" />' % href)
		except Exception:
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


class Comment(models.Model):
	"""
	评论
	"""
	title = models.CharField("标题", max_length=100)
	create_time = models.DateTimeField('评论时间', auto_now_add=True)
	user_name = models.CharField('评论用户', max_length=25)
	email = models.EmailField('预留邮箱', max_length=50, default='')
	url = models.CharField('链接', max_length=200)
	url_input = models.CharField('输入链接拼接', max_length=100, default='')  # 暂时未使用
	comment = models.TextField('评论内容', max_length=500)
	# 文章评论一对一
	post = models.ForeignKey(Article, related_name='post', default='', on_delete=models.CASCADE)

	class Meta:
		ordering = ['create_time']
		verbose_name = '评论'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.comment[:20]


class Subscription(models.Model):
	"""
	文章邮箱订阅
	"""
	email = models.EmailField(verbose_name='邮箱订阅用户', max_length=200)
	sub_time = models.DateTimeField(verbose_name='订阅时间', auto_now_add=True)

	class Meta:
		ordering = ['sub_time']
		verbose_name = '邮箱订阅'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.email


""""""""""""""""""""""""""" models监听器分割线 """""""""""""""""""""""""""""


# 创建用户时自动调用，绑定用户和用户信息
@receiver(post_save, sender=SiteUser)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserInfo.objects.create(username=instance)


# 注销用户时自动调用，删除对应用户信息
@receiver(pre_delete, sender=SiteUser)
def create_user_profile(sender, instance, **kwargs):
	instance.username = None


# 同步删除轮播图文件
@receiver(pre_delete, sender=Carousel)
def delete_upload_files(sender, instance, **kwargs):
	instance.carousel.delete(False)


# 同步删除文章大头图
@receiver(pre_delete, sender=ArticleImg)
def delete_upload_files(sender, instance, **kwargs):
	instance.article_img.delete(False)


# 同步删除捐助图
@receiver(pre_delete, sender=Pay)
def delete_upload_files(sender, instance, **kwargs):
	instance.payimg.delete(False)


# 同步删除网站logo
@receiver(pre_delete, sender=Conf)
def delete_upload_files(sender, instance, **kwargs):
	instance.website_logo.delete(False)

