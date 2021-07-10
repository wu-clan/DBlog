# -*- coding: utf-8 -*-

import importlib
from djangoProject import blogroll
from blog.models import Category, Article, Conf, Pay, Tag, Comment


def sidebar(request):
    # 所有文章类型
    category_list = Category.objects.all()

    # 文章排行
    blog_top = Article.objects.all().values("id", "title", "view").order_by('-view')[0:6]

    # 标签
    tag_list = Tag.objects.all()

    # 评论
    comment = Comment.objects.all().order_by('-create_time')[0:6]

    # 友链
    importlib.reload(blogroll)

    # 捐助首款图
    payimg = Pay.objects.all()

    # 网站配置
    conf_list = Conf.objects.all()

    return {
        'category_list': category_list,
        'blog_top': blog_top,
        'tag_list': tag_list,
        'comment_list': comment,
        'blogroll': blogroll.sites,
        'conf_list': conf_list,
        'payimg_list': payimg,
    }


if __name__ == '__main__':
    pass
