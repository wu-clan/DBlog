# -*- coding: utf-8 -*-
# Create your views here.
import hashlib
import random

import markdown
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from typing import List

from blog.comment.forms import CommentForm
from blog.models import About, SiteUser, Subscription
from blog.models import Article, Category, Tag, UserInfo
from blog.subscription.form import SubscriptionForm
from blog.user.forms import EditUserInfo, ProfileForm, RegisterForm, RestCodeForm, RestPwdForm, UserForm
from djangoProject import settings
from djangoProject.util import PageInfo


def index(request):
	"""
	主页
	"""
	_blog_list = Article.objects.all().order_by('-date_time')[0:6]
	_blog_hot = Article.objects.all().order_by('-view')[0:3]
	return render(request, 'blog/index.html', {"blog_list": _blog_list, "blog_hot": _blog_hot})


def get_page(request):
	"""
	分页
	"""
	page_number = request.GET.get("page")
	return 1 if not page_number or not page_number.isdigit() else int(page_number)


def hash_code(_hash, salt='050721..'):
	"""
	加密
	@salt:加点盐更强大
	"""
	data = hashlib.sha256()
	_hash += salt
	data.update(_hash.encode(encoding='utf-8'))
	return data.hexdigest()


def user_login(request):
	"""
	用户登录
	"""
	# 登录请求
	if request.method == "POST":
		login_form = UserForm(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			try:
				user = SiteUser.objects.get(username=username)
				# 哈希值和数据库内的值进行比对
				if user.password == hash_code(password):
					# 往session字典内写入用户状态和数据
					request.session['is_login'] = True
					request.session['user_id'] = user.id
					request.session['user_name'] = user.username
					# 登陆成功返回主页
					return redirect('/blog')
				else:
					messages.error(request, "密码不正确~")
			except:
				messages.error(request, "用户不存在~")
	else:
		login_form = UserForm()
	return render(request, 'blog/user/login.html', locals())


def user_register(request):
	"""
	用户注册
	"""
	# 注册请求
	if request.method == "POST":
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			username = register_form.cleaned_data['username']
			password1 = register_form.cleaned_data['password1']
			password2 = register_form.cleaned_data['password2']
			email = register_form.cleaned_data['email']
			# 密码验证
			if password1 != password2:
				messages.error(request, '两次密码输入不匹配，请重新输入')
				return redirect(reverse('blog:register'))
			else:
				same_name_user = SiteUser.objects.filter(username=username)
				if same_name_user:  # 用户名唯一
					messages.error(request, '用户名已经存在，请重新选择用户名！')
					return redirect(reverse('blog:register'))
				same_email_user = SiteUser.objects.filter(email=email)
				if same_email_user:  # 邮箱地址唯一
					messages.error(request, '该邮箱地址已经被注册过啦，请使用其他邮箱吧！')
					return redirect(reverse('blog:register'))
				# 数据没有问题，创建新用户并保存到数据库
				new_user = SiteUser.objects.create(
					username=username,
					password=hash_code(password1),
					email=email,
				)
				new_user.save()
				messages.success(request, '注册成功，请登录')
				return redirect(reverse('blog:login'))
	else:
		register_form = RegisterForm()
	return render(request, 'blog/user/register.html', locals())


def password_reset(request):
	"""
	密码重置
	"""
	return render(request, 'blog/password_reset/password_reset.html')


def reset_code(random_length=6):
	"""
	密码重置随机验证码
	"""
	str_code = ''
	chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	length = len(chars) - 1
	for i in range(random_length):
		str_code += chars[random.randint(0, length)]
	return str_code


def password_reset_email(request):
	"""
	密码重置验证码
	"""
	if request.method == "POST":
		rest_pwd_form = RestCodeForm(request.POST)
		if rest_pwd_form.is_valid():
			username_email = rest_pwd_form.cleaned_data['username_email']
			# 调试的时候请将此 try 方法注释，改为只是用 if 判断
			try:
				user = SiteUser.objects.filter(Q(username=username_email) | Q(email=username_email))
				if user:
					mail_receiver = user[0].email
					email_title = "重置密码"
					code = reset_code()  # 验证码
					request.session["code"] = code  # 将验证码保存到session
					email_body = "您的重置密码验证码为：{0}\n为了不影响您正常使用，请在24小时之内完成密码重置".format(code)
					send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, (mail_receiver,),
					                        auth_user=settings.EMAIL_HOST_USER,
					                        auth_password=settings.EMAIL_HOST_PASSWORD)
					messages.success(request, "验证码已发送，请查收邮件")
					return redirect(reverse('blog:password_reset_base'))
			except Exception:
				messages.error(request, '验证码发送失败，请联系网站管理员吧')
			else:
				messages.error(request, '用户名或邮箱不存在')
	else:
		rest_pwd_form = RestCodeForm()
	return render(request, 'blog/password_reset/password_reset_email.html', locals())


def password_reset_base(request):
	"""
	密码重置主页
	"""
	if request.method == 'POST':
		rest_pwd_form = RestPwdForm(request.POST)
		if rest_pwd_form.is_valid():
			password1 = rest_pwd_form.cleaned_data['password1']
			password2 = rest_pwd_form.cleaned_data['password2']
			code = rest_pwd_form.cleaned_data['reset_code']
			if password1 == password2:
				if code == request.session["code"]:
					new_user = SiteUser.objects.update(
						password=hash_code(password2)
					)
					del request.session["code"]  # 删除session
					# messages.success(request, "密码已重置")
					return redirect(reverse('blog:password_reset_done'))
				else:
					messages.error(request, '验证码错误')
			else:
				messages.error(request, '密码输入不一致，请重新输入')
	else:
		rest_pwd_form = RestPwdForm()
	return render(request, 'blog/password_reset/password_reset_base.html', locals())


def password_reset_done(request):
	"""
	重置结束
	"""
	return render(request, 'blog/password_reset/password_reset_done.html')


def user_logout(request):
	"""
	用户退出
	"""
	if not request.session.get('is_login', None):
		# 如果没登录，就不能登出
		return redirect('/blog')
	# 或者使用下面的方法
	request.session.flush()
	# del request.session['is_login']
	# del request.session['user_id']
	# del request.session['user_name']
	return redirect('/blog')


def user_delete(request, id):
	"""
	用户注销
	"""
	if request.method == 'POST':
		user = SiteUser.objects.get(id=id)
		curr_user = request.session.get('user_name')
		# 验证用户是否匹配，只有登录者才能执行注销
		if curr_user == user.username:
			# 注销用户，返回主页
			request.session.flush()
			user.delete()
			messages.success(request, '注销账户成功')
			return redirect('/blog')
		else:
			messages.error(request, '非注销账户登录，您没有权限执行注销操作')
			return redirect('/blog')
	else:
		return redirect('/blog')


# 编辑用户信息
def profile_edit(request, id):
	user = SiteUser.objects.get(id=id)
	old_email = user.email
	userinfo = UserInfo.objects.get(username_id=id)
	# u_sex = userinfo.sex
	# if u_sex == 0:
	# 	u_sex = '女'
	# else:
	# 	u_sex = '男'
	if request.method == 'POST':
		# 更新邮箱
		user_form = EditUserInfo(request.POST, instance=user)
		if user_form.is_valid():
			new_email = user_form.cleaned_data['email']
			if new_email != old_email:
				user_email = SiteUser.objects.filter(email=new_email)
				if user_email:
					messages.error(request, '该邮箱地址已经被注册过了，请使用其他邮箱吧！')
				user.save()
		# 更新用户信息
		profile_form = ProfileForm(request.POST, instance=userinfo)
		if profile_form.is_valid():
			avatar = profile_form.cleaned_data['avatar']
			mobile = profile_form.cleaned_data['mobile']
			# sex = profile_form.cleaned_data['sex']
			wechart = profile_form.cleaned_data['wechart']
			qq = profile_form.cleaned_data['qq']
			blog_address = profile_form.cleaned_data['blog_address']
			introduction = profile_form.cleaned_data['introduction']
			userinfo.save()
			messages.success(request, '更新个人信息成功')
			return redirect('blog:edituser', id=id)
	else:
		user_form = EditUserInfo()
		profile_form = ProfileForm()
	return render(request, 'blog/user/edituser.html', locals())


""""""""""""""""""""""""" 登录结束 """""""""""""""""""""""""


def detail(request, pk):
	"""
	博文详情
	"""
	blog = get_object_or_404(Article, pk=pk)
	blog.viewed()
	# Markdown渲染文章(含目录)，注意Markdown的 M 大小写
	md = markdown.Markdown(
		extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.fenced_code',
			'markdown.extensions.tables',
			'markdown.extensions.toc',
		]
	)
	# md文章内容
	blog.content = md.convert(blog.content)
	# form = CommentForm()
	# 获取对应文章的全部评论，倒序显示
	comments = blog.post.all().order_by('-create_time')
	context = {
		"blog": blog,
		'toc': md.toc,
		# 'form': form,
		'comments': comments
	}
	return render(request, 'blog/detail.html', context=context)


def blog_list(request):
	"""
	文章列表
	"""
	page_number = get_page(request)
	blog_count = Article.objects.count()
	page_info = PageInfo(page_number, blog_count)
	_blog_list = Article.objects.all()[page_info.index_start: page_info.index_end]
	return render(request, 'blog/list.html', {"blog_list": _blog_list, "page_info": page_info})


def category(request, name):
	"""
	文章分类
	"""
	categories = Category.fetch_all_category()

	page_number = get_page(request)
	blog_count = Article.objects.filter(category__name=name).count()
	page_info = PageInfo(page_number, blog_count)
	_blog_list = Article.objects.filter(category__name=name)[page_info.index_start: page_info.index_end]
	return render(request, 'blog/category.html', {
		"blog_list": _blog_list,
		"page_info": page_info,
		"category": name,
		'categories': categories
	})


def tag(request, name):
	"""
	标签
	"""
	page_number = get_page(request)
	blog_count = Article.objects.filter(tag__tag_name=name).count()
	page_info = PageInfo(page_number, blog_count)
	_blog_list = Article.objects.filter(tag__tag_name=name)[page_info.index_start: page_info.index_end]
	return render(request, 'blog/tag.html', {"blog_list": _blog_list,
	                                         "tag": name,
	                                         "page_info": page_info})


def archive(request):
	"""
	文章归档
	"""
	_blog_list = Article.objects.values("id", "title", "date_time").order_by('-date_time')
	archive_dict = {}
	for blog in _blog_list:
		pub_month = blog.get("date_time").strftime("%Y年%m月")
		if pub_month in archive_dict:
			archive_dict[pub_month].append(blog)
		else:
			archive_dict[pub_month] = [blog]
	data = sorted([{"date": _[0], "blogs": _[1]} for _ in archive_dict.items()], key=lambda item: item["date"],
	              reverse=True)
	return render(request, 'blog/archive.html', {"data": data})


def about(request):
	"""
	关于（包含统计图）
	"""
	# markdown渲染自我介绍
	about = About.objects.all().first()
	if about:
		about.contents = markdown.markdown(about.contents,
		                                   extensions=[
			                                   'markdown.extensions.extra',
			                                   'markdown.extensions.fenced_code',
			                                   'markdown.extensions.tables',
		                                   ]
		                                   )

	# 统计图准备
	articles = Article.objects.filter().all().order_by('-date_time')
	categories = Category.fetch_all_category()
	if not articles or not categories:
		# 没有文章或者分类的情况
		return render(request, 'blog/about.html', {'articles': None, 'categories': None})
	# 发布统计
	all_date = articles.values('date_time')
	# 计算最近一年的时间list作为坐标横轴 注意时间为 例如[2019-5] 里面不是2019-05
	latest_date = all_date[0]['date_time']
	end_year = latest_date.strftime("%Y")
	end_month = latest_date.strftime("%m")
	date_list = []
	for i in range(int(end_month), 13):
		date = str(int(end_year) - 1) + '-' + str(i)
		date_list.append(date)
	for j in range(1, int(end_month) + 1):
		date = end_year + '-' + str(j)
		date_list.append(date)
	value_list = []
	all_date_list = []
	for i in all_date:
		# 这里直接格式化 去掉月份前面的0, !! window使用%#m, mac和linux使用%-m !!
		try:
			all_date_list.append(i['date_time'].strftime('%Y-%-m'))
		except ValueError:
			all_date_list.append(i['date_time'].strftime('%Y-%#m'))
	for i in date_list:
		value_list.append(all_date_list.count(i))

	# 饼图统计
	temp_list = []  # 临时集合
	tags_list = []  # 存放每个标签对应的文章数
	tags = Tag.objects.all()
	for tag in tags:
		temp_list.append(tag.tag_name)
		temp_list.append(len(tag.article_set.all()))
		tags_list.append(temp_list)
		temp_list = []
	# 根据文章数排序
	tags_list.sort(key=lambda x: x[1], reverse=True)

	# top10统计
	top10_tags = []
	top10_tags_values = []
	for i in tags_list[:10]:
		top10_tags.append(i[0])
		top10_tags_values.append(i[1])

	return render(request, 'blog/about.html', locals())


def search(request):
	"""
	搜索
	"""
	key = request.GET['key']
	page_number = get_page(request)
	blog_count = Article.objects.filter(title__icontains=key).count()
	page_info = PageInfo(page_number, blog_count)
	_blog_list = Article.objects.filter(title__icontains=key)[page_info.index_start: page_info.index_end]
	return render(request, 'blog/search.html', {"blog_list": _blog_list, "pages": page_info, "key": key})


# def get_comment(request, pk):
# 	"""
# 	评论数据
# 	"""
# 	blog = get_object_or_404(Article, pk=pk)
# 	blog.commenced()
# 	result = {'status': 'error', 'content': '请求失败'}
# 	if request.method == 'POST':
# 		form = CommentForm(request.POST)
# 		if form.is_valid():
# 			comment = form.save(commit=False)
# 			comment.title = blog.title
# 			# 文章跳转url
# 			# url = request.get_full_path()
# 			url = request.headers['Referer']
# 			comment.url = str(url)
# 			# 关联评论与文章
# 			comment.post = blog
# 			comment.save()
# 			result['status'] = 'success'
# 			result['content'] = '评论保存成功'
# 		else:
# 			return JsonResponse(result)
# 	else:
# 		result['content'] = '请求类型错误，请使用POST'
# 		return JsonResponse(result)


def get_comment(request, pk):
	"""
	评论数据
	"""
	blog = get_object_or_404(Article, pk=pk)
	blog.commenced()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.title = blog.title
			# 文章跳转url
			# url = request.get_full_path()
			url = request.headers['Referer']
			comment.url = str(url)
			# 关联评论与文章
			comment.post = blog
			comment.save()
			return redirect('blog:get_comment', pk=pk)
	# 不是 post 请求，重定向到文章详情页。
	return redirect('blog:detail', pk=pk)


def subscription_record(request):
	"""
	邮箱订阅记录
	"""
	if request.method == 'POST':
		form = SubscriptionForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			try:
				_email = Subscription.objects.filter(Q(email=email))
				if _email:
					messages.success(request, '此邮箱已经订阅过啦')
					return redirect('blog:subscription_record')
				else:
					sub = form.save(commit=False)
					sub.save()
					return redirect('blog:subscription_record')
			except ValueError:
				messages.error(request, '订阅失败')
	messages.success(request, '订阅成功，发布新文章后会通过邮箱及时通知你哟')
	return redirect('/blog')


@receiver(post_save, sender=Article)
def send_stu_email(sender, created, **kwargs):
	"""
	文章发布监听器，发布文章时触发并直接发送邮件订阅通知
	"""
	if created:
		blog = Article.objects.filter()
		if blog:
			link_id = blog.count()
			title = blog.values('title').first().get('title').strip()
			# 文章链接
			# 本地调试时请将 settings.website_author_link 换成 http://127.0.0.1:端口号
			link = settings.website_author_link + '/blog/detail/{id}'.format(id=link_id)
			_email = Subscription.objects.filter().values_list('email', flat=True)
			if _email:
				email_list = _email[:99999999]
				email_title = "文章订阅推送"
				email_body = "你订阅的 %s: %s 的博客发布新文章啦，快点击链接查阅吧\n文章：%s\n链接：%s" \
				             % (settings.website_author, settings.website_author_link, title, link)
				try:
					send_mail(email_title, email_body, settings.EMAIL_HOST_USER, email_list,
					          auth_user=settings.EMAIL_HOST_USER,
					          auth_password=settings.EMAIL_HOST_PASSWORD)
				except Exception:
					# 发送失败默认不发送，不影响发布文章
					print('发送文章订阅邮件失败，请调试检查！！！')
					pass


def unsubscribe(request):
	"""
	取消邮箱订阅
	"""


# 1，点击取消订阅跳转确认界面
# 2，确认取消，调用数据库，删除此订阅邮箱


def page_not_found_error(request, exception):
	return render(request, "404.html", status=404)


def page_error(request):
	return render(request, "404.html", status=500)
