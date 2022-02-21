from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin

from blog.models import About, Article, ArticleImg, Carousel, Category, Comment, Conf, Friend, Pay, \
    Subscription, Tag, UserInfo, HeadAnnouncement, MainAnnouncement

# Register your models here.
admin.site.unregister(User)


class UserInfoAdmin(admin.StackedInline):
    """
    行内 admin 表
    """
    model = UserInfo
    can_delete = False


@admin.register(User)
class SiteUserAdmin(UserAdmin):
    """
    重新注册 User
    """
    inlines = (
        UserInfoAdmin,
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    订阅
    """
    list_display = (
        'email',
        'sub_time'
    )


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """
    关于
    """
    list_display = (
        'contents',
    )


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """
    友链
    """
    list_display = (
        'url',
        'title',
        'name'
    )


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """
    首页轮播图配置
    """
    list_display = (
        'link',
        'carousel_title',
        'carousel',
        'img_link_title',
        'img_alt'
    )


@admin.register(HeadAnnouncement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    公告
    """
    list_display = (
        'head_announcement',
    )


@admin.register(MainAnnouncement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    公告
    """
    list_display = (
        'main_announcement',
    )


@admin.register(Conf)
class ConfAdmin(ImportExportModelAdmin):
    """
    网站配置信息
    """
    list_display = (
        'main_website',
        'website_number',
        'name',
        'chinese_description',
        'english_description',
        'email',
        'website_logo'
    )
    fieldsets = (
        ('网站配置信息', {
            'fields': (
                'main_website',
                'website_number',
                'website_logo'
            )
        }),
        ('作者信息', {
            'fields': (
                'name',
                'chinese_description',
                'english_description',
                'avatar_link',
                'website_author',
                'website_author_link',
                'email',
                'git'
            )
        }),
    )


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    """
    收款图
    """
    list_display = (
        'payimg',
    )


@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    """
    文章
    """
    date_hierarchy = 'date_time'
    list_display = (
        'title',
        'category',
        'date_time',
        'content_validity',
        'digest',
        'author',
        'view',
        'comment',
        'picture'
    )
    list_filter = ('category', 'author')
    filter_horizontal = ('tag',)


@admin.register(ArticleImg)
class ArticleImgAdmin(admin.ModelAdmin):
    """
    文章大头图
    """
    list_display = (
        'img_title',
        'url',
        'images',
        'article_img',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    文章类型
    """
    list_display = (
        'name',
        'created_time',
        'last_mod_time'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签
    """
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    评论
    """
    list_display = (
        'title',
        'create_time',
        'user_name',
        'email',
        'request_ip',
        'request_address',
        'comment_validity',
        'url',
        'avatar_link',
        'url_input',
    )
    search_fields = ('user_name',)
