# -*- coding: utf-8 -*-

from blog.models import Announcement, Carousel, Category, Article, Conf, Friend, Pay, Tag, Comment
from djangoProject import settings


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
    friends = Friend.objects.all()

    # 捐助首款图
    payimg = Pay.objects.all().order_by('-payimg')[0:2]

    # 轮播图
    carousel = Carousel.objects.all()

    # 公告
    announcement = Announcement.objects.all()

    return {
        'category_list': category_list,
        'blog_top': blog_top,
        'tag_list': tag_list,
        'comment_list': comment,
        'friends': friends,
        'payimg_list': payimg,
        'carousel_list': carousel,
        'announcement_list': announcement
    }


def website_conf(request):
    # 网站配置
    conf_list = Conf.objects.all()[0:1]
    conf_list_redis = Conf.fetch_all_site_info()

    if conf_list_redis:
        return {
            'main_website': conf_list_redis.main_website,
            'name': conf_list_redis.name,
            'chinese_description': conf_list_redis.chinese_description,
            'english_description': conf_list_redis.english_description,
            'avatar_link': conf_list_redis.avatar_link,
            'website_author': conf_list_redis.website_author,
            'website_author_link': conf_list_redis.website_author_link,
            'email': conf_list_redis.email,
            'website_number': conf_list_redis.website_number,
            'git': conf_list_redis.git,
            'website_logo': conf_list_redis.website_logo,
            'config_list':conf_list,
        }
    else:
        return {
            'main_website': settings.main_website,
            'name': settings.name,
            'chinese_description': settings.chinese_description,
            'english_description': settings.english_description,
            'avatar_link': settings.avatar_link,
            'website_author': settings.website_author,
            'website_author_link': settings.website_author_link,
            'email': settings.email,
            'website_number': settings.website_number,
            'git': settings.git,
            'website_logo': settings.website_logo,
            'config_list': conf_list,
        }


if __name__ == '__main__':
    pass
