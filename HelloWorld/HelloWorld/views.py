#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@Time : 2020/11/25
@Author : w
@File : views
@Software :
"""
# from django.http import HttpResponse

# def hello(request):
#     return HttpResponse('不讲武德！')

# 模板
# from django.shortcuts import render
#
# def runoob(request):
#     context = {}
#     context['hello'] = '不讲武德！'
#     return render(request, 'runoob.html', context)

# 变量
# from django.shortcuts import render
#
# def runoob(request):
#     views_name = '不讲武德'
#     return render(request, 'runoob.html', {'name':views_name})

# 列表
# from django.shortcuts import render
#
# def runoob(request):
#     views_list = ['马保国','不讲武德','耗子尾汁']
#     return render(request, 'runoob.html', {'name':views_list})

# 字典
from django.shortcuts import render

def runoob(request):
    views_dict = {'name':"马保国"}
    return render(request, 'runoob.html', {'views_dict': views_dict})


