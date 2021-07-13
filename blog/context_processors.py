# -*- coding: utf-8 -*-


from blog.models import Announcement, Carousel, Category, Article, Conf, Friend, Pay, Tag, Comment


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

    # 网站配置
    conf_list = Conf.objects.all()[0:1]

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
        'conf_list': conf_list,
        'payimg_list': payimg,
        'carousel_list': carousel,
        'announcement_list': announcement
    }


if __name__ == '__main__':
    pass
