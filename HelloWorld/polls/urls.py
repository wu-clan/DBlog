#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/28 0:20
# @Author  : wu
# @Site    :
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index')
]