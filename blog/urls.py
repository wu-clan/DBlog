# -*- coding: utf-8 -*-
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
    # 博文详情
    path('detail/<int:pk>/', views.detail, name='detail'),
    # 文章归档
    path('archive/', views.archive, name='archive'),
    # 搜索
    path('search/', views.search, name='search'),
    # 评论
    path('get_comment/<int:pk>/', views.get_comment, name='get_comment'),
    # 二级评论
    path('get_comment/<int:pk>/<int:parent_comment_id>/', views.get_comment, name='comment_reply'),
    # 关于
    path('about/', views.about, name='about'),
    # Rss
    path('rss/', rss.DBlogRssFeed(), name='rss'),
    # Atom
    path('atom/', rss.DBlogAtomFeed(), name='atom'),
    # 邮箱订阅
    path('subscription_record/', views.subscription_record, name='subscription_record'),
    # 取消订阅跳转
    path('begin_unsub/', views.begin_unsub, name='begin_unsub'),
    # 取消订阅
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),

    # 用户操作
    # 登录
    path('login/', views.user_login, name='login'),
    # 注册
    path('register/', views.user_register, name='register'),
    # 密码重置跳转
    path('password_reset/', views.password_reset, name='password_reset'),
    # 密码重置
    path('password_reset_base/', views.password_reset_base, name='password_reset_base'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_email/', views.password_reset_email, name='password_reset_email'),
    # 退出登录
    path('logout/', views.user_logout, name='logout'),
    # 用户信息
    path('edit_user/<int:pk>/', views.profile_edit, name='edit_user'),
    # 删除用户头像
    path('delete/avatar/<int:pk>/', views.delete_avatar, name='delete_avatar'),
    # 注销用户
    path('delete/<int:pk>/', views.user_delete, name='delete'),

]
