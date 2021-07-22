# -*- coding: utf-8 -*-

__author__ = 'xiaowu'

from blog import views
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
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('register/', views.register, name='register'),
]

