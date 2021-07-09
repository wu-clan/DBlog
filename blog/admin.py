from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin
from blog.models import Tag, Article, Category, Comment, Pay, Conf


@admin.register(Conf)
class ConfAdmin(ImportExportModelAdmin):
    list_display = (
        'home_title',
        'record_number',
        'carousel_announcement',
        'announcement',
        'website_designer',
        'design_author_hyperlink',
        'receiving_email_address',
        'title',
        'chinese_description',
        'english_description',
        'avatar_hyperlink',
    )
    fieldsets = (
        ('网站配置信息', {
            'fields': (
                'home_title',
                'record_number',
            )
        }),
        ('公告', {
            'fields': (
                'carousel_announcement',
                'announcement',
            )
        }),
        ('作者信息', {
            'fields': (
                'website_designer',
                'design_author_hyperlink',
                'receiving_email_address',
                'title',
                'chinese_description',
                'english_description',
                'avatar_hyperlink',
            )
        }),
    )


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = (
        'payvximg',
        'payaliimg'
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
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
    list_display = (
        'name',
        'created_time',
        'last_mod_time'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'source_id',
        'create_time',
        'user_name',
        'url',
        'comment'
    )
