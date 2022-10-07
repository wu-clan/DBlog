# -*- coding: utf-8 -*-
from blog.models import ArticleImg, Carousel, Category, Article, Conf, Friend, Pay, Tag, Comment, \
    HeadAnnouncement, MainAnnouncement
from djangoProject import settings


def sidebar(request):
    # 所有文章类型
    category_list = Category.objects.all()

    # 文章大头图
    article_img = ArticleImg.objects.all()

    # 文章排行
    blog_top = Article.objects.all().values("id", "title", "view").order_by('-view')[0:10]

    # 标签
    tag_list = Tag.objects.all()

    # 评论
    comment = Comment.objects.all().order_by('-created_time')[0:5]

    # 友链
    friends = Friend.objects.all()

    # 捐助收款图
    pay_img = Pay.objects.all()[0:2]

    # 轮播图
    carousel = Carousel.objects.all()

    # 公告
    head_announcement = HeadAnnouncement.objects.all()
    main_announcement = MainAnnouncement.objects.all()

    return {
        'category_list': category_list,
        'article_img': article_img,
        'blog_top': blog_top,
        'tag_list': tag_list,
        'comment_list': comment,
        'friends': friends,
        'pay_img_list': pay_img,
        'carousel_list': carousel,
        'head_announcement_list': head_announcement,
        'main_announcement_list': main_announcement,
    }


def website_conf(request):
    # 网站配置
    conf_by_redis = Conf.fetch_all_site_info()

    if conf_by_redis:
        return {
            'main_website': conf_by_redis.main_website,
            'name': conf_by_redis.name,
            'chinese_description': conf_by_redis.chinese_description,
            'english_description': conf_by_redis.english_description,
            'avatar_link': conf_by_redis.avatar_link,
            'website_author': conf_by_redis.website_author,
            'website_author_link': conf_by_redis.website_author_link,
            'email': conf_by_redis.email,
            'website_number': conf_by_redis.website_number,
            'git': conf_by_redis.git,
            'website_logo': conf_by_redis.website_logo,
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
        }
