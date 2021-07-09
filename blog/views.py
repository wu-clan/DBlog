# -*- coding: utf-8 -*-
# Create your views here.

import json
from django.http import JsonResponse

from djangoProject.util import PageInfo
from blog.models import Article, Comment, Conf, Pay
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404


def web_conf(request):
    """
    网站配置
    """
    conf_list = Conf.objects.all()

    return render(request, 'blog/right.html', {
        'conf': conf_list,
        # 'HOME_TITLE': conf_list.home_title,
        # 'CAROUSEL_ANNOUNCEMENT': conf_list.carousel_announcement,
        # 'ANNOUNCEMENT': conf_list.announcement,
        # 'TITLE': conf_list.title,
        # 'CHINESE_DESC': conf_list.chinese_description,
        # 'ENGLISH_DESC': conf_list.english_description,
        # 'AVATAR_LINK': conf_list.avatar_hyperlink,
        # 'WEBSITE_DESIGNER': conf_list.website_designer,
        # 'DESIGN_AUTHOR_LINK': conf_list.design_author_hyperlink,
        # 'RECEIVING_EMAIL_ADDRESS': conf_list.receiving_email_address,
        # 'RECORD_NUMBER': conf_list.record_number,
    })


def pay(request):
    """
    捐助收款图
    """
    imglist = Pay.objects.all()

    return render(request, 'blog/right.html', {
        # 'payimg': imglist
        locals()
    })


def get_page(request):
    page_number = request.GET.get("page")
    return 1 if not page_number or not page_number.isdigit() else int(page_number)


def index(request):
    _blog_list = Article.objects.all().order_by('-date_time')[0:5]
    _blog_hot = Article.objects.all().order_by('-view')[0:6]
    return render(request, 'blog/index.html', {"blog_list": _blog_list, "blog_hot": _blog_hot})


def blog_list(request):
    """
    列表
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
    分类
    :param request:
    :param name:
    :return:
    """
    page_number = get_page(request)
    blog_count = Article.objects.filter(category__name=name).count()
    page_info = PageInfo(page_number, blog_count)
    _blog_list = Article.objects.filter(category__name=name)[page_info.index_start: page_info.index_end]
    return render(request, 'blog/category.html', {"blog_list": _blog_list, "page_info": page_info,
                                                  "category": name})


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
    关于
    """
    return render(request, 'blog/about.html', {"about": "aboutme"})


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


