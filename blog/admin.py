from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin
from blog.models import Announcement, Carousel, Friend, Tag, Article, Category, Comment, Pay, Conf


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
        'carousel',
        'carousel_title',
        'img_link_title',
        'img_alt'
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    公告
    """
    list_display = (
        'head_announcement',
        'main_announcement'
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
class ArticleAdmin(admin.ModelAdmin):
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
        'source_id',
        'create_time',
        'user_name',
        'url',
        'comment'
    )
