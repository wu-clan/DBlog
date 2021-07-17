# -*- coding: utf-8 -*-
# Create your views here.

import json

from django.core.paginator import PageNotAnInteger, Paginator
from django.http import JsonResponse

from djangoProject.util import PageInfo
from blog.models import Article, Category, Comment, Tag
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404


def get_page(request):
    page_number = request.GET.get("page")
    return 1 if not page_number or not page_number.isdigit() else int(page_number)


def index(request):
    _blog_list = Article.objects.all().order_by('-date_time')[0:5]
    _blog_hot = Article.objects.all().order_by('-view')[0:6]
    return render(request, 'blog/index.html', {"blog_list": _blog_list, "blog_hot": _blog_hot})


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
        return render(request, 'blog/about.html', {
            'articles': None,
            'categories': None,
        })

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
        # 这里直接格式化 去掉月份前面的0 使用%#m
        all_date_list.append(i['date_time'].strftime('%Y-%#m'))

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


