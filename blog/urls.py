# -*- coding: utf-8 -*-

__author__ = 'xiaowu'

from blog import rss, views
from django.urls import path

urlpatterns = [
	path('', views.index, name='index'),
	# 博客列表
	path('list/', views.blog_list, name='list'),
	# 标签
	path('tag/<str:name>/', views.tag, name='tag'),
	# 分类
	path('category/<str:name>/', views.category, name='category'),
	# 细节（图标，分享等...）
	path('detail/<int:pk>/', views.detail, name='detail'),
	# 文章归档
	path('archive/', views.archive, name='archive'),
	# 搜索
	path('search/', views.search, name='search'),
	# 留言表单
	path('message/', views.message, name='message'),
	# 评论
	path('get_comment/', views.get_comment, name='get_comment'),
	# 关于
	path('about/', views.about, name='about'),
	# Rss
	path('rss/', rss.DBlogRssFeed(), name='rss'),
	# Atom
	path('atom/', rss.DBlogAtomFeed(), name='atom'),

	###########
	# 用户操作 #
	###########
	# 登录
	path('login/', views.user_login, name='login'),
	# 登录校验
	path('is_login_backend/', views.is_login_backend, name='is_login_backend'),
	# 注册
	path('register/', views.user_register, name='register'),
	# 密码重置
	path('password_reset', views.password_reset, name='password_reset'),
	path('password_reset_done', views.password_reset_done, name='password_reset_done'),
	# 退出登录
	path('logout/', views.user_logout, name='logout'),
	# 用户信息
	path('edituser/<int:id>/', views.profile_edit, name='edituser'),
	# 注销用户
	path('delete/<int:id>/', views.user_delete, name='delete'),

]
