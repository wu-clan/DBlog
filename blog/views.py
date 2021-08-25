# -*- coding: utf-8 -*-
# Create your views here.
import hashlib
import json
import random
import string

import markdown
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from blog.comment.forms import CommentForm
from blog.models import SiteUser
from blog.user.forms import ProfileForm, RegisterForm, RestCodeForm, RestPwdForm, UserForm
from djangoProject import settings
from djangoProject.util import PageInfo
from blog.models import Article, Category, Comment, UserInfo, Tag
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404


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
			try:
				user = SiteUser.objects.filter(Q(username=username_email) | Q(email=username_email))
				if user:
					mail_receiver = user[0].email
					email_title = "重置密码"
					code = reset_code()  # 验证码
					request.session["code"] = code  # 将验证码保存到session
					email_body = "您的重置密码验证码为：{0}\n为了不影响您正常使用，请在24小时之内完成重置".format(code)
					send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, (mail_receiver,),
					                        auth_user=settings.EMAIL_HOST_USER,
					                        auth_password=settings.EMAIL_HOST_PASSWORD)
					messages.success(request, "验证码已发送，请查收邮件")
					return redirect(reverse('blog:password_reset_base'))
			# 调试的时候请将此expect注释
			except WindowsError:
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
			return redirect('/blog')
		else:
			messages.error(request, '非注销账户登录，您没有权限执行注销操作')
			return redirect('/blog')
	else:
		return redirect('/blog')


# 编辑用户信息
def profile_edit(request, id):
	user = SiteUser.objects.get(id=id)
	profile_form = ProfileForm(request.POST)
	if request.method == 'POST':
		if profile_form.is_valid():
			avatar = profile_form.cleaned_data['avatar']
			mobile = profile_form.cleaned_data['mobile']
			sex = profile_form.cleaned_data['sex']
			wechart = profile_form.cleaned_data['wechart']
			qq = profile_form.cleaned_data['qq']
			blog_address = profile_form.cleaned_data['blog_address']
			introduction = profile_form.cleaned_data['introduction']
			siteinfo = UserInfo.objects.update(
				avatar=avatar,
				mobile=mobile,
				sex=sex,
				wechart=wechart,
				qq=qq,
				blog_address=blog_address,
				introduction=introduction
			)
			messages.success(request, '更新个人信息成功')
			return redirect('/')
		else:
			messages.error(request, '输入信息有误，请检查')
	else:
		profile_form = ProfileForm()
	return render(request, 'blog/user/edituser.html', locals())


""""""""""""""""""""""""" 登录结束 """""""""""""""""""""""""


def detail(request, pk):
	"""
	博文详情
	"""
	blog = get_object_or_404(Article, pk=pk)
	blog.viewed()
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
	form = CommentForm()
	# 获取这篇 post 下的全部评论
	comment_list = blog.post.all()
	context = {
		"blog": blog,
		'toc': md.toc,
		'form': form,
		'comment_list': comment_list
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


def message(request):
	"""
	留言
	"""
	return render(request, 'blog/message_board.html', {"source_id": "message"})


def about(request):
	"""
	关于（包含统计图）
	"""
	articles = Article.objects.filter(category=True).all().order_by('-date_time')
	categories = Category.fetch_all_category()

	if not articles or not categories:
		# 没有文章或者分类的情况
		return render(request, 'blog/about.html', {'articles': None, 'categories': None})

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

	# for i in all_date:
	#     # 这里直接格式化 去掉月份前面的0, !! window使用%#m, mac和linux使用%-m !!
	#     all_date_list.append(i['date_time'].strftime('%Y-%?m'))
	# 换个方法吧，调试出来的
	all_date_list.append(date_list[-1])

	for i in date_list:
		value_list.append(all_date_list.count(i))
	temp_list = []  # 临时集合
	tags_list = []  # 存放每个标签对应的文章数
	tags = Tag.objects.all()
	for tag in tags:
		temp_list.append(tag.tag_name)
		temp_list.append(len(tag.article_set.all()))
		tags_list.append(temp_list)
		temp_list = []

	tags_list.sort(key=lambda x: x[1], reverse=True)  # 根据文章数排序

	top10_tags = []
	top10_tags_values = []
	for i in tags_list[:10]:
		top10_tags.append(i[0])
		top10_tags_values.append(i[1])

	return render(request, 'blog/about.html', {
		'articles': articles,
		'categories': categories,
		'tags': tags,
		'date_list': date_list,
		'value_list': value_list,
		'top10_tags': top10_tags,
		'top10_tags_values': top10_tags_values
	})


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


# @csrf_exempt
# def get_comment(request):
# 	"""
# 	接收畅言的评论回推， post方式回推
# 	记得去畅言配置回推地址 http://网站地址/blog/get_comment/
# 	启用SSL的网站使用 https
# 	"""
# 	arg = request.POST
# 	data = arg.get('data')
# 	data = json.loads(data)
# 	title = data.get('title')
# 	url = data.get('url')
# 	source_id = data.get('sourceid')
# 	if source_id not in ['message']:
# 		article = Article.objects.get(pk=source_id)
# 		article.commenced()
# 	comments = data.get('comments')[0]
# 	content = comments.get('content')
# 	user = comments.get('user').get('nickname')
# 	Comment(title=title, source_id=source_id, user_name=user, url=url, comment=content).save()
# 	return JsonResponse({"status": "ok"})

def get_comment(request, pk):
	"""
	评论
	"""
	blog = get_object_or_404(Article, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			# 关联评论与文章
			comment.post = blog
			comment.save()
			return redirect('blog:get_comment', pk=pk)
	# 不是 post 请求，重定向到文章详情页。
	return redirect('blog:detail', pk=pk)


def page_not_found_error(request, exception):
	return render(request, "404.html", status=404)


def page_error(request):
	return render(request, "404.html", status=500)
