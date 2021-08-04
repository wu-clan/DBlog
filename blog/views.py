# -*- coding: utf-8 -*-
# Create your views here.
import hashlib
import json
import random
import string

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from blog.models import SiteUser
from blog.user.forms import ProfileForm, RegisterForm, UserForm
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
					return redirect(reverse('blog:is_login_backend'))
				else:
					messages.error(request, "密码不正确~")
			except:
				messages.error(request, "用户不存在~")
		else:
			return render(request, 'blog/user/login.html', locals())
	# 如果是不是POST请求，返回登陆表单
	login_form = UserForm()
	return render(request, 'blog/user/login.html', locals())


def is_login_backend(request):
	"""
	后端登录验证
	"""
	# 这里必须用读取字典的get()方法把is_login的value缺省设置为False，当用户访问backend这个url先尝试获取这个浏览器对应
	# 的session中的 is_login 的值。如果对方登录成功的话，在login里就已经把is_login的值修改为了True,反之这个值就是False的
	is_login = request.session.get('is_login', False)
	if is_login:
		cookie_content = request.COOKIES
		session_content = request.session
		is_login_username = request.session['user_name']
		user_id = request.session['user_id']
		return render(request, 'blog/base.html', locals())
	else:
		return redirect(reverse('blog:login'))


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
	# 如果请求不是POST，则渲染一个空的表单。
	register_form = RegisterForm()
	return render(request, 'blog/user/register.html', locals())


def password_reset(request):
	"""
	密码重置
	"""
	return render(request, 'password_reset/password_reset.html')


def password_reset_done(request):
	"""
	重置结束
	"""
	return render(request, 'password_reset/password_reset_done.html')


def user_logout(request):
	if not request.session.get('is_login', None):
		# 如果没登录，就不能登出
		return redirect('/')
	# 或者使用下面的方法
	request.session.flush()
	# del request.session['is_login']
	# del request.session['user_id']
	# del request.session['user_name']
	return redirect('/')


@login_required(login_url='blog/login/')
def user_delete(request):
	"""
	用户注销
	"""
	if request.method == 'POST':
		user = SiteUser.objects.get(id=id)
		# 验证用户是否匹配，只有登录者才能执行注销
		if request.username == user:
			# 注销用户，返回主页
			logout(request)
			user.delete()
			return redirect('/')
		else:
			return HttpResponse('非此账户登录者，没有权限执行注销操作~')
	else:
		return redirect('/')


# 编辑用户信息
@login_required(login_url='blog/login/')
def profile_edit(request, id):
	user = SiteUser.objects.get(id=id)
	# user_id 是 OneToOneField 自动生成的字段
	if UserInfo.objects.filter(user_id=id).exists():
		profile = UserInfo.objects.get(user_id=id)
	else:
		profile = UserInfo.objects.create(user=user)

	if request.method == 'POST':
		# 验证修改数据者，是否为用户本人
		if request.user != user:
			messages.error(request, '非本人账户，无法修改个人信息')
			return redirect('blog:edituser.html')

		profile_form = ProfileForm(request.POST, request.FILES)
		if profile_form.is_valid():
			# 取得清洗后的合法数据
			profile_cd = profile_form.cleaned_data
			# 用户信息保存
			profile.avatar = profile_cd['avatar']
			profile.mobile = profile_cd['mobile']
			profile.sex = profile_cd['sex']
			profile.wechart = profile_cd['wechart']
			profile.qq = profile_cd['qq']
			profile.blog_address = profile_cd['blog_address']
			profile.introduction = profile_cd['introduction']
			if 'avatar' in request.FILES:
				profile.avatar = profile_cd["avatar"]
			profile.save()
			# 带参数的 redirect()
			return redirect("blog:edituser", id=id)
		else:
			messages.error(request, '信息输入有误，请重新输入！')
			return redirect(reverse('blog:edituser.html'))
	profile_form = ProfileForm()
	return render(request, 'blog/user/edituser.html', locals())


""""""""""""""""""""""""" 登录结束 """""""""""""""""""""""""


def blog_list(request):
	"""
	文章列表
	:param request:
	:return:
	"""
	page_number = get_page(request)
	blog_count = Article.objects.count()
	page_info = PageInfo(page_number, blog_count)
	_blog_list = Article.objects.all()[page_info.index_start: page_info.index_end]
	return render(request, 'blog/list.html', {"blog_list": _blog_list, "page_info": page_info})


def category(request, name):
	"""
	文章分类
	:param request:
	:param name:
	:return:
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
	:param request:
	:param name
	:return:
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
	:param request:
	:return:
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


@csrf_exempt
def get_comment(request):
	"""
	接收畅言的评论回推， post方式回推
	记得去畅言配置回推地址 http://网站地址/blog/get_comment/
	启用SSL的网站使用 https
	:param request:
	:return:
	"""
	arg = request.POST
	data = arg.get('data')
	data = json.loads(data)
	title = data.get('title')
	url = data.get('url')
	source_id = data.get('sourceid')
	if source_id not in ['message']:
		article = Article.objects.get(pk=source_id)
		article.commenced()
	comments = data.get('comments')[0]
	content = comments.get('content')
	user = comments.get('user').get('nickname')
	Comment(title=title, source_id=source_id, user_name=user, url=url, comment=content).save()
	return JsonResponse({"status": "ok"})


def detail(request, pk):
	"""
	博文详情
	:param request:
	:param pk:
	:return:
	"""
	blog = get_object_or_404(Article, pk=pk)
	blog.viewed()
	return render(request, 'blog/detail.html', {"blog": blog})


def search(request):
	"""
	搜索
	:param request:
	:return:
	"""
	key = request.GET['key']
	page_number = get_page(request)
	blog_count = Article.objects.filter(title__icontains=key).count()
	page_info = PageInfo(page_number, blog_count)
	_blog_list = Article.objects.filter(title__icontains=key)[page_info.index_start: page_info.index_end]
	return render(request, 'blog/search.html', {"blog_list": _blog_list, "pages": page_info, "key": key})


def page_not_found_error(request, exception):
	return render(request, "404.html", status=404)


def page_error(request):
	return render(request, "404.html", status=500)
