# -*- coding: utf-8 -*-

__author__ = 'xiaowu'

from blog import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.blog_list, name='list'),
    path('tag/<str:name>/', views.tag, name='tag'),
    path('category/<str:name>/', views.category, name='category'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('archive/', views.archive, name='archive'),
    path('search/', views.search, name='search'),
    path('message/', views.message, name='message'),
    path('getComment/', views.get_comment, name='get_comment'),
    path('about/', views.about, name='about'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('register/', views.register, name='register'),
]

